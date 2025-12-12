#!/usr/bin/env python3
import numpy as np
import yaml
import h5py
import os
import warnings

warnings.simplefilter("always", DeprecationWarning)
warnings.formatwarning = lambda msg, *args, **kwargs: f"{msg}\n"

PARSER_VERSION = "0.2.15"

SUPPORTED_REPRESENTATIONS = {"canonical"}  # extend this set when adding new representations
SUPPORTED_CONTENT = {"all", "metadata", "fields", "wavefunctions"} # New supported content types

#----------------------------------------------------------
def _ensure_version(metadata):
    """Ensure the metadata contains the current parser version."""
    metadata["version"] = PARSER_VERSION
    return metadata


def _get_representation(wf_meta):
    rep = wf_meta.get("representation", "canonical")

    if not isinstance(rep, str):
        raise ValueError("representation must be a string")

    rep_norm = rep.lower().strip()

    if rep_norm not in SUPPORTED_REPRESENTATIONS:
        raise ValueError(f"Unknown wavefunction representation '{rep}'. "
                         f"Supported: {SUPPORTED_REPRESENTATIONS}")

    return rep_norm


def _sanitize_metadata(data):
    """
    Recursively convert NumPy objects (arrays, scalars) in a dictionary
    to native Python types (list, float, int) for clean YAML dumping.
    """
    if isinstance(data, dict):
        return {k: _sanitize_metadata(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        # Handle lists/tuples, which often contain the field metadata lists
        return [_sanitize_metadata(item) for item in data]
    elif isinstance(data, np.ndarray):
        # Convert NumPy arrays to lists of native Python types
        return data.tolist()
    elif isinstance(data, np.generic):
        # Convert NumPy scalar types (e.g., np.float64) to native Python types (float)
        return data.item()
    else:
        return data


#----------------------------------------------------------
def write_hdf5(data, filepath):
    """
    Write a Bogoliubov state and associated fields to an HDF5 file.

    Arrays are written in Fortran (column-major) order for consistency
    with the Fortran-based binary format.
    """
    metadata = data['metadata'].copy()
    metadata = _ensure_version(metadata)

    prefix = metadata.pop('prefix', None)
    if prefix is None:
        raise ValueError("Missing 'prefix' in metadata; cannot determine HDF5 filename.")

    odir = os.path.dirname(filepath) or '.'
    os.makedirs(odir, exist_ok=True)

    fields = metadata.pop('field', None)

    with h5py.File(filepath, 'w') as h5f:
        # Save global metadata. Sanitize before dumping to ensure clean YAML string.
        sanitized_metadata = _sanitize_metadata(metadata.copy())
        h5f.attrs['metadata_yaml'] = yaml.dump(sanitized_metadata)

        # Save field data
        if fields is not None:
            fld_group = h5f.create_group('field')
            for fld in fields:
                key = fld['name']
                if key not in data:
                    continue
                arr = np.asfortranarray(data[key])
                dset = fld_group.create_dataset(key, data=arr, compression='gzip')

                # Copy field-specific metadata. Sanitize field metadata attributes.
                sanitized_fld = _sanitize_metadata(fld.copy())
                for k, v in sanitized_fld.items():
                    if k not in ('name', 'suffix'):
                        dset.attrs[k] = v

        # Save wavefunctions
        if 'wavefunction' in metadata:
            wf_meta = metadata['wavefunction']
            rep = _get_representation(wf_meta)

            wf_group = h5f.create_group('wavefunction')
            wf_group.attrs['representation'] = rep

            match rep:
                case "canonical":
                    # --- Neutron block ---
                    neu_group = wf_group.create_group('neutron')
                    if 'statesn' in data:
                        neu_group.create_dataset('states',
                                                 data=np.asfortranarray(data['statesn']),
                                                 compression='gzip')
                    if 'un' in data:
                        neu_group.create_dataset('u', data=np.asfortranarray(data['un']), compression='gzip')
                    if 'vn' in data:
                        neu_group.create_dataset('v', data=np.asfortranarray(data['vn']), compression='gzip')

                    # --- Proton block ---
                    pro_group = wf_group.create_group('proton')
                    if 'statesp' in data:
                        pro_group.create_dataset('states',
                                                 data=np.asfortranarray(data['statesp']),
                                                 compression='gzip')
                    if 'up' in data:
                        pro_group.create_dataset('u', data=np.asfortranarray(data['up']), compression='gzip')
                    if 'vp' in data:
                        pro_group.create_dataset('v', data=np.asfortranarray(data['vp']), compression='gzip')

                case _:
                    raise ValueError(f"Unsupported representation '{rep}'.")


#----------------------------------------------------------
def read_hdf5(filepath, content="all"):
    """
    Read a Bogoliubov state and fields from an HDF5 file.
    Restores a metadata dictionary compatible with the binary/YAML format.

    content: "all" (default), "metadata", "fields", or "wavefunctions"
    """
    if content not in SUPPORTED_CONTENT:
        raise ValueError(f"Unknown content type '{content}'. Supported: {SUPPORTED_CONTENT}")

    data = {}
    with h5py.File(filepath, 'r') as h5f:
        metadata_yaml = h5f.attrs['metadata_yaml']
        metadata = yaml.safe_load(metadata_yaml)

        prefix = os.path.splitext(os.path.basename(filepath))[0]
        metadata['prefix'] = prefix
        metadata = _ensure_version(metadata)
        data['metadata'] = metadata
        
        if content == 'metadata':
            return data

        # Field data
        if content in ("all", "fields", "wavefunctions"):
            fld_group = None
            if 'field' in h5f:
                fld_group = h5f['field']
            elif 'variables' in h5f:
                fld_group = h5f['variables']
                warnings.warn("HDF5 group 'variables' is deprecated; use 'field' instead.", DeprecationWarning)

            if fld_group is not None and content in ("all", "fields"):
                fields = []
                for key, dset in fld_group.items():
#                   data[key] = np.array(dset, order='F')
                    data[key] = np.asarray(dset)
                    fld_meta = {}
                    for k, v in dset.attrs.items():
                        if isinstance(v, np.generic):
                            v = v.item()
                        fld_meta[k] = v
                    fld_meta['name'] = key
                    fld_meta['suffix'] = f"_{key}.bin"
                    fields.append(fld_meta)
                metadata['field'] = fields
            elif fld_group is not None and 'field' in metadata:
                 # If only reading WFs but fields exist in metadata, check for old 'variables'
                 # group and copy field metadata if 'field' is not present but 'variables' is.
                 # This is to ensure minimal necessary metadata for WF section is available.
                 pass
            
            # Wavefunctions
            if 'wavefunction' in h5f and content in ("all", "wavefunctions"):
                wf_group = h5f['wavefunction']

                # representation from file (optional)
                rep_in_file = wf_group.attrs.get("representation", None)

                if 'wavefunction' in metadata:
                    # prefer metadata
                    rep = _get_representation(metadata['wavefunction'])
                    if rep_in_file and rep_in_file != rep:
                        warnings.warn(
                            f"Representation mismatch: metadata='{rep}', file='{rep_in_file}'. "
                            f"Using metadata.",
                            DeprecationWarning
                        )
                else:
                    # fallback if metadata lacks wf section
                    rep = rep_in_file or "canonical"
                    metadata['wavefunction'] = {'representation': rep} # Add minimal wf metadata

                match rep:
                    case "canonical":
                        if 'neutron' in wf_group:
                            neu_group = wf_group['neutron']
                            if 'states' in neu_group:
                                data['statesn'] = np.asarray(neu_group['states'])
                            if 'u' in neu_group:
                                data['un'] = np.asarray(neu_group['u'])
                            if 'v' in neu_group:
                                data['vn'] = np.asarray(neu_group['v'])

                        if 'proton' in wf_group:
                            pro_group = wf_group['proton']
                            if 'states' in pro_group:
                                data['statesp'] = np.asarray(pro_group['states'])
                            if 'u' in pro_group:
                                data['up'] = np.asarray(pro_group['u'])
                            if 'v' in pro_group:
                                data['vp'] = np.asarray(pro_group['v'])

                    case _:
                        raise ValueError(f"Unsupported representation '{rep}'.")

    return data


#----------------------------------------------------------
def write_yaml(data, filepath):
    """
    Write Bogoliubov state and fields to YAML + binary format.
    Ensures binary arrays are written in strict Fortran (column-major) order.
    """
    metadata = _ensure_version(data['metadata'])
    prefix = metadata['prefix']
    odir = os.path.dirname(filepath) or '.'
    os.makedirs(odir, exist_ok=True)

    # Sanitize metadata before dumping to prevent NumPy-specific serialization
    sanitized_metadata = _sanitize_metadata(metadata.copy())

    # Write YAML metadata
    with open(filepath, 'w') as file:
        yaml.dump(sanitized_metadata, file)

    # Write fields
    if 'field' in metadata:
        fields = metadata['field']
        for fld in fields:
            key = fld['name']
            if key not in data:
                continue

            array = data[key]
            f_name = os.path.join(odir, prefix + fld['suffix'])
            with open(f_name, 'wb') as f:
                f.write(np.asfortranarray(array).tobytes(order='F'))

    #------------------------------------------------------
    # Wavefunctions
    if 'wavefunction' in metadata:
        wf_meta = metadata['wavefunction']
        rep = _get_representation(wf_meta)

        f_name = os.path.join(odir, prefix + wf_meta['suffix'])

        match rep:
            case "canonical":
                with open(f_name, 'wb') as file:
                    # Only write if all required keys are present
                    required_keys = ['statesn', 'statesp', 'un', 'vn', 'up', 'vp']
                    if all(k in data for k in required_keys):
                        buffer = (
                            data['statesn'].tobytes(order='F') +
                            data['statesp'].tobytes(order='F') +
                            data['un'].tobytes() +
                            data['vn'].tobytes() +
                            data['up'].tobytes() +
                            data['vp'].tobytes()
                        )
                        file.write(buffer)
                    else:
                        print(f"Warning: Skipping wavefunction binary write for '{f_name}' due to missing data.")

            case _:
                raise ValueError(f"Unsupported wavefunction representation '{rep}'.")


#----------------------------------------------------------
def read_yaml(odir, header, content="all"):
    """
    Read a Bogoliubov state and fields (potentials, densities)
    from YAML + binary format.

    content: "all" (default), "metadata", "fields", or "wavefunctions"
    """
    if content not in SUPPORTED_CONTENT:
        raise ValueError(f"Unknown content type '{content}'. Supported: {SUPPORTED_CONTENT}")

    data = {}
    with open(header, 'r') as file:
        metadata = yaml.safe_load(file)
        metadata = _ensure_version(metadata)
        data['metadata'] = metadata

    if 'variables' in metadata:
        warnings.warn("YAML key 'variables' is deprecated; using 'field' instead.", DeprecationWarning)
        metadata['field'] = metadata.pop('variables')

    if content == 'metadata':
        return data

    prefix = metadata['prefix']
    nx, ny, nz = metadata['nx'], metadata['ny'], metadata['nz']
    symmetry = metadata.get('symmetry', '')
    if symmetry == 'ev8':
        nx, ny, nz = nx // 2, ny // 2, nz // 2

    # Read Fields
    if content in ("all", "fields"):
        n_frames = metadata.get('frame', 1)
        if 'field' in metadata:
            fields = metadata['field']
            valid_fields = []
            for fld in fields:
                key = fld['name']
                f_name = os.path.join(odir, prefix + fld['suffix'])
                nc = fld['n_components']
                try:
                    with open(f_name, 'rb'):
                        pass
                except FileNotFoundError:
                    print(f"Warning: missing field file '{f_name}', skipping.")
                    continue

                if n_frames == 1:
                    shape = (nx, ny, nz, nc)
                    if nc == 1:
                        shape = (nx, ny, nz)
                else:
                    shape = (nx, ny, nz, nc, n_frames)
                    if nc == 1:
                        shape = (nx, ny, nz, n_frames)

                data[key] = np.reshape(np.fromfile(f_name, dtype=np.float64), shape, order='F')
                valid_fields.append(fld)

            metadata['field'] = valid_fields

    # Read Wavefunctions
    if content in ("all", "wavefunctions"):
        if 'wavefunction' in metadata:
            wf_meta = metadata['wavefunction']
            rep = _get_representation(wf_meta)

            f_name = os.path.join(odir, prefix + wf_meta['suffix'])
            nw_n = wf_meta['n_neutron_states']
            nw_p = wf_meta['n_proton_states']

            match rep:
                case "canonical":
                    try:
                        with open(f_name, 'rb') as file:

                            statesn_bsize = nw_n * nx * ny * nz * 2 * np.complex128(0).nbytes
                            buffer = file.read(statesn_bsize)
                            data['statesn'] = np.reshape(np.frombuffer(buffer, dtype=np.complex128),
                                                         (nx, ny, nz, 2, nw_n), order='F')

                            statesp_bsize = nw_p * nx * ny * nz * 2 * np.complex128(0).nbytes
                            buffer = file.read(statesp_bsize)
                            data['statesp'] = np.reshape(np.frombuffer(buffer, dtype=np.complex128),
                                                         (nx, ny, nz, 2, nw_p), order='F')

                            un_bsize = nw_n * np.complex128(0).nbytes
                            data['un'] = np.frombuffer(file.read(un_bsize), dtype=np.complex128)
                            data['vn'] = np.frombuffer(file.read(un_bsize), dtype=np.complex128)

                            up_bsize = nw_p * np.complex128(0).nbytes
                            data['up'] = np.frombuffer(file.read(up_bsize), dtype=np.complex128)
                            data['vp'] = np.frombuffer(file.read(up_bsize), dtype=np.complex128)

                    except FileNotFoundError:
                        print(f"Warning: missing wavefunction file '{f_name}', skipping wavefunction read.")
                        # If file is missing, we still return the metadata
                        pass
                case _:
                    raise ValueError(f"Unsupported representation '{rep}'.")

    return data


#----------------------------------------------------------
# Unified interface
def read(filepath, content="all"):
    """
    Auto-detect file type and read accordingly.
      - .yaml/.yml -> YAML format
      - .h5/.hdf5  -> HDF5 format

    content: "all" (default), "metadata", "fields", or "wavefunctions"
    """
    if content not in SUPPORTED_CONTENT:
        raise ValueError(f"Unknown content type '{content}'. Supported: {SUPPORTED_CONTENT}")
        
    if filepath.endswith(('.yaml', '.yml')):
        odir = os.path.dirname(filepath) or '.'
        return read_yaml(odir, filepath, content=content)
    elif filepath.endswith(('.h5', '.hdf5')):
        return read_hdf5(filepath, content=content)
    else:
        raise ValueError(f"Unrecognized file extension for '{filepath}'.")


def write(data, filepath):
    """
    Unified writer. File format is determined by the extension of `filepath`.
    """
    ext = os.path.splitext(filepath)[1].lower()
    data['metadata'] = _ensure_version(data['metadata'])
    if ext in ('.yaml', '.yml'):
        write_yaml(data, filepath)
    elif ext in ('.h5', '.hdf5'):
        write_hdf5(data, filepath)
    else:
        raise ValueError(f"Unknown file extension for output: '{filepath}'. Expected .yaml/.yml or .h5/.hdf5.")
