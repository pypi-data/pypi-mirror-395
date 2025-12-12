#!/usr/bin/env python3
"""
ev8_to_ev1.py

Convert MOCCa EV8 dataset (with spatial symmetries) into EV1 (full box, no symmetry).
"""

import os
import sys
import numpy as np

try:
    import saclay_format as saclay_parser
except ImportError:
    import saclay_parser


# ===============================================================
# --- Symmetry utilities ---
# ===============================================================

def Complete_3D(nx, ny, nz, F, symx=1, symy=1, symz=1):
    """Reconstruct full 3D array from EV8-like quadrant."""
    if abs(symx) == 1:
        newx = 2 * nx
    elif symx == 0:
        newx = nx
    else:
        raise ValueError
    if abs(symy) == 1:
        newy = 2 * ny
    elif symy == 0:
        newy = ny
    else:
        raise ValueError
    if abs(symz) == 1:
        newz = 2 * nz
        offz = nz
    elif symz == 0:
        newz = nz
        offz = 0
    else:
        raise ValueError

    complete = np.zeros((newx, newy, newz), dtype=F.dtype)

    complete[nx:, ny:, offz:] = F
    complete[:nx, ny:, offz:] = np.flip(F, axis=0) * symx
    complete[nx:, :ny, offz:] = np.flip(F, axis=1) * symy
    if symz != 0:
        complete[nx:, ny:, :nz] = np.flip(F, axis=2) * symz
        complete[:nx, :ny, offz:] = np.flip(F, axis=(0, 1)) * symx * symy
        complete[:nx, ny:, :nz] = np.flip(F, axis=(0, 2)) * symx * symz
        complete[nx:, :ny, :nz] = np.flip(F, axis=(1, 2)) * symy * symz
        complete[:nx, :ny, :nz] = np.flip(F, axis=(0, 1, 2)) * symx * symy * symz

    return complete


def get_EV8_symmetries_spwfs():
    """Return (sx, sy, sz) symmetry arrays for spwfs blocks."""
    sx = np.zeros((4, 4))
    sy = np.zeros((4, 4))
    sz = np.zeros((4, 4))

    # BLOCK 1
    sx[:, 0] = [1, -1, -1, 1]
    sy[:, 0] = [1, -1, 1, -1]
    sz[:, 0] = [1, 1, -1, -1]

    # BLOCK 3
    sx[:, 2] = [1, -1, -1, 1]
    sy[:, 2] = [1, -1, 1, -1]
    sz[:, 2] = [-1, -1, 1, 1]

    return sx, sy, sz


def complex_to_real_spwfs(array):
    r_array = np.zeros((array.shape[0], array.shape[1], array.shape[2], 4, array.shape[4]), dtype=np.float64)
    r_array[:, :, :, 0, :] = np.real(array[:, :, :, 0, :])
    r_array[:, :, :, 1, :] = np.imag(array[:, :, :, 0, :])
    r_array[:, :, :, 2, :] = np.real(array[:, :, :, 1, :])
    r_array[:, :, :, 3, :] = np.imag(array[:, :, :, 1, :])
    return r_array


def real_to_complex_spwfs(array):
    c_array = np.zeros((array.shape[0], array.shape[1], array.shape[2], 2, array.shape[4]), dtype=np.complex128)
    c_array[:, :, :, 0, :] = array[:, :, :, 0, :] + 1j * array[:, :, :, 1, :]
    c_array[:, :, :, 1, :] = array[:, :, :, 2, :] + 1j * array[:, :, :, 3, :]
    return c_array


def convert_array_EV8_EV1(array, nx, ny, nz, symx, symy, symz, nc=1):
    if nc != 1:
        full_array = np.zeros((2 * nx, 2 * ny, 2 * nz, nc), dtype=array.dtype)
        for idx in range(nc):
            full_array[..., idx] = Complete_3D(nx, ny, nz, array[..., idx], symx[idx], symy[idx], symz[idx])
    else:
        full_array = Complete_3D(nx, ny, nz, array, symx[0], symy[0], symz[0])
    return full_array


def break_syms_spwfs(states, symblocks, nx, ny, nz):
    """Convert spwfs from EV8 to EV1."""
    states = complex_to_real_spwfs(states)
    sx, sy, sz = get_EV8_symmetries_spwfs()

    c_states = np.zeros((2 * nx, 2 * ny, 2 * nz, 4, states.shape[-1]))
    si = 0
    for B in range(4):
        N = symblocks[B]
        for i in range(N):
            for k in range(4):
                c_states[:, :, :, k, si + i] = Complete_3D(nx, ny, nz, states[:, :, :, k, si + i],
                                                           symx=sx[k, B], symy=sy[k, B], symz=sz[k, B])
        si += N

    return real_to_complex_spwfs(c_states)


# ===============================================================
# --- Main conversion function ---
# ===============================================================

def ev8_to_ev1(data):
    """Convert EV8 dataset to EV1 (full box). Returns modified data."""
    if data["metadata"].get("symmetry", "").lower() != "ev8":
        raise ValueError("Input data symmetry is not EV8")

    ev1_data = data.copy()
    ev1_data["metadata"]["symmetry"] = "ev1"

    nx = data["metadata"]["nx"] // 2
    ny = data["metadata"]["ny"] // 2
    nz = data["metadata"]["nz"] // 2

    # --- Convert fields ---
    for field in data["metadata"].get("field", []):
        key = field["name"]
        nc = field["n_components"]
        sx = np.asarray(field["sx"])
        sy = np.asarray(field["sy"])
        sz = np.asarray(field["sz"])
        ev1_data[key] = convert_array_EV8_EV1(data[key], nx, ny, nz, sx, sy, sz, nc)

    # --- Convert spwfs ---
    wf_meta = data["metadata"]["wavefunction"]
    ev1_data["statesn"] = break_syms_spwfs(data["statesn"], wf_meta["symblocks_n"], nx, ny, nz)
    ev1_data["statesp"] = break_syms_spwfs(data["statesp"], wf_meta["symblocks_p"], nx, ny, nz)

    # --- Update prefix ---
    prefix = os.path.splitext(ev1_data["metadata"].get("prefix", "ev1"))[0]
    ev1_data["metadata"]["prefix"] = prefix

    return ev1_data


# ===============================================================
# --- Minimal main ---
# ===============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert EV8 dataset to EV1 (full box)")
    parser.add_argument("input", help="Input file (.yaml/.yml or .h5/.hdf5)")
    parser.add_argument("-o", "--output", help="Output file (default: overwrite input)")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output or input_path

    if not os.path.exists(input_path):
        print(f"Input file '{input_path}' not found.")
        sys.exit(1)

    data = saclay_parser.read(input_path)
    data_ev1 = ev8_to_ev1(data)

    # Update extension if missing
    if not os.path.splitext(output_path)[1]:
        ext = os.path.splitext(input_path)[1]
        output_path += ext

    print(f"Writing EV1 data to '{output_path}'")
    saclay_parser.write(data_ev1, output_path)
    print("Done.")


if __name__ == "__main__":
    main()
