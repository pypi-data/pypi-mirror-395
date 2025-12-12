#!/usr/bin/env python3
"""
compute_densities.py

Compute neutron/proton densities from canonical wavefunctions stored
in saclay-format YAML+binary or HDF5 files.

Only works if:
  - representation is 'canonical'
  - symmetry is 'none' or 'cr1'
"""

import os
import sys
import argparse
import numpy as np

try:
    import saclay_format as saclay_parser
except ImportError:
    import saclay_parser


OCC_WARNING_THRESHOLD = 0.5
SUPPORTED_REPRESENTATION = "canonical"
SUPPORTED_SYMMETRIES = {"none", "cr1"}


# ===============================================================
# Core computations
# ===============================================================

def compute_density(states, v_occ):
    """Compute spatial density rho(r) from canonical wavefunctions."""
    # states shape: (nx, ny, nz, 2, n_states)
    rho = np.sum(np.abs(states)**2, axis=3)          # sum over spin
    rho = np.tensordot(rho, np.abs(v_occ)**2, axes=([3], [0]))  # sum over states
    return np.real(rho)


def compute_and_check(data, key_states, key_v, label, dx, dy, dz, N_meta, thr):
    """Compute rho_n or rho_p and check particle-number consistency."""
    if key_states not in data or key_v not in data:
        print(f"{label}: missing wavefunctions. Skipped.")
        return

    print(f"Computing {label} ...")

    rho = compute_density(data[key_states], data[key_v])
    data[label] = rho

    # Check particle number
    N_calc = float(np.sum(rho) * dx * dy * dz)
    print(f"{label}_calc = {N_calc:.6f}")

    if abs(N_calc - N_meta) > thr:
        print(f"Warning: metadata={N_meta}, computed={N_calc:.6f} "
              f"(diff {N_calc - N_meta:.6f})")


def add_density_fields_to_metadata(data):
    """Ensure rho_n and rho_p appear in metadata['field']."""
    meta = data.setdefault("metadata", {})
    fields = meta.setdefault("field", [])

    def add_field(name):
        if name in data and not any(f.get("name") == name for f in fields):
            fields.append({
                "name": name,
                "n_components": 1,
                "suffix": f"_{name}.bin"
            })

    add_field("rho_n")
    add_field("rho_p")


# ===============================================================
# Main compute_densities(data)
# ===============================================================

def compute_densities(data, threshold=OCC_WARNING_THRESHOLD):
    """
    Compute neutron and proton densities and update `data` in place.
    Returns the modified `data`.
    """

    meta = data.get("metadata", {})

    # --- representation check ---
    wf_meta = meta.get("wavefunction", {})
    representation = wf_meta.get("representation", "canonical").lower()
    if representation != SUPPORTED_REPRESENTATION:
        raise ValueError(f"Unsupported representation '{representation}'")

    # --- symmetry check ---
    symmetry = meta.get("symmetry", "none").lower()
    if symmetry not in SUPPORTED_SYMMETRIES:
        raise ValueError(f"Unsupported symmetry '{symmetry}'")

    # Grid spacings and particle numbers
    dx = float(meta.get("dx", 1.0))
    dy = float(meta.get("dy", 1.0))
    dz = float(meta.get("dz", 1.0))
    N_meta = float(meta.get("N", 0))
    Z_meta = float(meta.get("Z", 0))

    # Compute densities
    compute_and_check(data, "statesn", "vn", "rho_n", dx, dy, dz, N_meta, threshold)
    compute_and_check(data, "statesp", "vp", "rho_p", dx, dy, dz, Z_meta, threshold)

    # Add fields to metadata
    add_density_fields_to_metadata(data)

    return data


# ===============================================================
# Minimal main
# ===============================================================

def main():
    parser = argparse.ArgumentParser(description="Compute densities from canonical wavefunctions")
    parser.add_argument("input", help="Input file (.yaml/.yml or .h5/.hdf5)")
    parser.add_argument("-o", "--output", help="Output file (default: overwrite input)")
    parser.add_argument("-t", "--threshold", type=float,
                        default=OCC_WARNING_THRESHOLD,
                        help="Warning threshold for particle-number mismatch")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output or input_path

    if not os.path.exists(input_path):
        print(f"Error: file '{input_path}' not found.")
        sys.exit(1)

    print(f"Reading: {input_path}")
    data = saclay_parser.read(input_path)

    # *** Single call ***
    data = compute_densities(data, threshold=args.threshold)

    # Update prefix (needed by saclay_format)
    base = os.path.basename(output_path)
    data.setdefault("metadata", {})["prefix"] = os.path.splitext(base)[0]

    print(f"Writing output: {output_path}")
    saclay_parser.write(data, output_path)
    print("Done.")


if __name__ == "__main__":
    main()
