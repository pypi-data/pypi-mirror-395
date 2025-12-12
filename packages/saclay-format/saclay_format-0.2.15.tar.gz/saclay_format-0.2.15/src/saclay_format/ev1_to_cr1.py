#!/usr/bin/env python3
"""
ev1_to_cr1.py

Convert MOCCa EV1 dataset (no spatial symmetry) into CR1 (Kramers partners).
"""

import os
import sys
import numpy as np

try:
    import saclay_format as saclay_parser
except ImportError:
    import saclay_parser


# ===============================================================
# --- Utilities ---
# ===============================================================

def kramers_partner(states):
    """
    Construct Kramers partners for 2-spinor wavefunctions:
        psi_T = i sigma_y psi* -> ( psi_down*, -psi_up* )
    Input shape:  (nx, ny, nz, 2, nw)
    Output shape: (nx, ny, nz, 2, nw)
    """
    conj = np.conjugate(states)
    up   = conj[..., 0, :]
    dn   = conj[..., 1, :]
    partner = np.empty_like(states)
    partner[..., 0, :] = dn
    partner[..., 1, :] = -up
    return partner


def interleave_with_partners(states, partners):
    """Interleave original states and their Kramers partners along last axis."""
    shape = list(states.shape)
    shape[-1] *= 2
    interleaved = np.empty(shape, dtype=states.dtype)
    interleaved[..., ::2] = states
    interleaved[..., 1::2] = partners
    return interleaved


def interleave_amplitudes(arr):
    """Interleave array with its complex conjugate along first axis."""
    conj = np.conjugate(arr)
    shape = list(arr.shape)
    shape[0] *= 2
    interleaved = np.empty(shape, dtype=arr.dtype)
    interleaved[::2] = arr
    interleaved[1::2] = conj
    return interleaved


def check_orthonormality(states, tol=1e-10):
    """
    Check orthonormality of wavefunctions.
    states: shape (nx, ny, nz, 2, nw)
    """
    nx, ny, nz, _, nw = states.shape
    flat = states.reshape(-1, nw)
    overlaps = flat.conj().T @ flat
    norms = np.sqrt(np.real(np.diag(overlaps)))
    overlaps /= (norms[:, None] * norms[None, :])
    deviation = np.max(np.abs(overlaps - np.eye(nw)))
    print("Max deviation from orthonormality: {:.2e}".format(deviation))
    if deviation > tol:
        print("Warning: orthonormality check FAILED")
    else:
        print("Orthonormality OK")


# ===============================================================
# --- Main conversion function ---
# ===============================================================

def ev1_to_cr1(data):
    """
    Translate EV1 or EV8 dataset into CR1 by doubling wavefunctions.
    - If the data is EV8, it is first converted to EV1.
    """
    sym = data["metadata"].get("symmetry", "").lower()

    if sym == "ev8":
        print("Input data is EV8, converting to EV1 first...")
        data = saclay_parser.ev8_to_ev1(data)
        sym = "ev1"

    if sym != "ev1":
        raise ValueError(f"Input data symmetry is '{sym}', expected 'ev1' or 'ev8'.")


    md    = data["metadata"].copy()
    wf_md = md.get("wavefunction", {}).copy()

    nw_n = wf_md["n_neutron_states"]
    nw_p = wf_md["n_proton_states"]

    # Build Kramers partners
    statesn_cr1 = interleave_with_partners(data["statesn"], kramers_partner(data["statesn"]))
    statesp_cr1 = interleave_with_partners(data["statesp"], kramers_partner(data["statesp"]))

    # Bogoliubov amplitudes
    un_cr1 = interleave_amplitudes(data["un"])
    vn_cr1 = interleave_amplitudes(data["vn"])
    up_cr1 = interleave_amplitudes(data["up"])
    vp_cr1 = interleave_amplitudes(data["vp"])

    # Update metadata
    md["symmetry"] = "cr1"
    md["prefix"]   = md.get("prefix", "run") + "_cr1"
    wf_md["n_neutron_states"] = 2 * nw_n
    wf_md["n_proton_states"]  = 2 * nw_p
    md["wavefunction"] = wf_md

    cr1_data = data.copy()
    cr1_data.update({
        "metadata": md,
        "statesn": statesn_cr1,
        "statesp": statesp_cr1,
        "un": un_cr1,
        "vn": vn_cr1,
        "up": up_cr1,
        "vp": vp_cr1
    })

    return cr1_data


# ===============================================================
# --- Minimal main ---
# ===============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert EV1 dataset to CR1 (Kramers partners)")
    parser.add_argument("input", help="Input file (.yaml/.yml or .h5/.hdf5)")
    parser.add_argument("-o", "--output", help="Output file (default: overwrite input)")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output or input_path

    if not os.path.exists(input_path):
        print(f"Input file '{input_path}' not found.")
        sys.exit(1)

    data = saclay_parser.read(input_path)
    data_cr1 = ev1_to_cr1(data)

    # Update extension if missing
    if not os.path.splitext(output_path)[1]:
        ext = os.path.splitext(input_path)[1]
        output_path += ext

    print(f"Writing CR1 data to '{output_path}'")
    saclay_parser.write(data_cr1, output_path)

    # Optional: check orthonormality
    print("\nChecking neutron states:")
    check_orthonormality(data_cr1["statesn"])
    print("Checking proton states:")
    check_orthonormality(data_cr1["statesp"])


if __name__ == "__main__":
    main()
