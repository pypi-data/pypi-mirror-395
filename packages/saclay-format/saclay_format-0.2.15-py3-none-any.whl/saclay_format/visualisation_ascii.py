#!/usr/bin/env python3
"""
visualisation_ascii.py
ASCII visualization of Saclay-format densities.

Defaults:
  - plane = xz
  - mode  = proj (integrate over the removed axis)
"""

import argparse
import numpy as np

CHARS = " .:-=+*#%@"

try:
    import saclay_format as saclay_parser
except ImportError:
    import saclay_parser


# ============================================================
# ASCII conversion
# ============================================================

def array_to_ascii(a, width=None, height=None, chars=CHARS):
    """Convert 2D array a to ASCII heatmap."""
    if width is not None and height is not None:
        a = downsample(a, width, height)

    amin, amax = np.min(a), np.max(a)
    if amax <= amin:
        amax = amin + 1.0

    norm = (a - amin) / (amax - amin)
    idx = (norm * (len(chars) - 1)).astype(int)
    lines = ["".join(chars[i] for i in row) for row in idx]
    return lines


def downsample(a, width, height):
    """Downsample 2D array by block averaging."""
    H, W = a.shape
    sy = max(1, H // height)
    sx = max(1, W // width)

    H2 = (H // sy) * sy
    W2 = (W // sx) * sx
    a = a[:H2, :W2]

    return a.reshape(H2 // sy, sy, W2 // sx, sx).mean(axis=(1, 3))


# ============================================================
# Slice / Projection operators
# ============================================================

def compute_plane(rho, plane, mode):
    """
    plane : 'xz', 'yz', 'xy'
    mode  : 'slice' or 'proj'
    rho   : array (nx, ny, nz)
    
    Modification: The result is transposed in all cases
    to achieve: First axis in plane name = Horizontal, Second axis = Vertical.
    (i.e., array shape (Second Axis, First Axis)).
    """
    nx, ny, nz = rho.shape

    if plane == "xz":
        # Original array shape: (X, Z)
        if mode == "slice":
            y0 = ny // 2
            return rho[:, y0, :].T # Transposed shape: (Z, X) -> X Horizontal, Z Vertical
        else:
            return rho.sum(axis=1).T # Transposed shape: (Z, X) -> X Horizontal, Z Vertical

    elif plane == "yz":
        # Original array shape: (Y, Z)
        if mode == "slice":
            x0 = nx // 2
            return rho[x0, :, :].T # Transposed shape: (Z, Y) -> Y Horizontal, Z Vertical
        else:
            return rho.sum(axis=0).T # Transposed shape: (Z, Y) -> Y Horizontal, Z Vertical

    elif plane == "xy":
        # Original array shape: (X, Y)
        if mode == "slice":
            z0 = nz // 2
            return rho[:, :, z0].T # Transposed shape: (Y, X) -> X Horizontal, Y Vertical
        else:
            return rho.sum(axis=2).T # Transposed shape: (Y, X) -> X Horizontal, Y Vertical

    else:
        raise ValueError(f"Unknown plane: {plane}")


# ============================================================
# Box layout
# ============================================================

def add_box(ascii_lines):
    """Add | and - around ASCII image."""
    if not ascii_lines:
        return ""

    width = len(ascii_lines[0])
    top = "+" + "-" * width + "+"
    bottom = top
    body = ["|" + line + "|" for line in ascii_lines]

    return "\n".join([top] + body + [bottom])


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="ASCII visualization of densities.")
    parser.add_argument("input", help="Input file (.h5/.yaml)")

    # Plane flags → optional, default is xz
    parser.add_argument("-xz", action="store_true", help="Show XZ plane (default)")
    parser.add_argument("-yz", action="store_true", help="Show YZ plane")
    parser.add_argument("-xy", action="store_true", help="Show XY plane")

    # Mode flags → optional, default is proj
    parser.add_argument("-slice", action="store_true", help="Central slice in the removed axis")
    parser.add_argument("-proj", action="store_true", help="Projection (integration) (default)")

    # Output size
    parser.add_argument("--width", type=int, default=120, help="ASCII width")
    parser.add_argument("--height", type=int, default=60, help="ASCII height")

    args = parser.parse_args()

    # ---------------------------------------------------------
    # Determine plane with default xz
    # ---------------------------------------------------------
    if not (args.xz or args.yz or args.xy):
        plane = "xz"
    else:
        selected = [p for p, f in [("xz", args.xz), ("yz", args.yz), ("xy", args.xy)] if f]
        if len(selected) != 1:
            print("ERROR: Choose only one plane: -xz -yz -xy")
            exit(1)
        plane = selected[0]

    # ---------------------------------------------------------
    # Determine mode with default proj
    # ---------------------------------------------------------
    if not (args.slice or args.proj):
        mode = "proj"
    elif args.slice and args.proj:
        print("ERROR: Choose exactly one of -slice OR -proj")
        exit(1)
    else:
        mode = "slice" if args.slice else "proj"

    # ---------------------------------------------------------
    # Load data
    # ---------------------------------------------------------
    data = saclay_parser.read(args.input, content='fields')
    fields = data["metadata"]["field"]

    if not any(var["name"] == "rho_n" for var in fields):
        print("rho_n not available.")
        exit(1)

    rho_n = data["rho_n"]
    n_frames = data["metadata"].get("frame", 1)

    print(f"Loaded: {args.input}")
    print(f"Plane = {plane}, Mode = {mode}")
    print(f"Frames = {n_frames}\n")

    # ---------------------------------------------------------
    # Loop over frames
    # ---------------------------------------------------------
    for frame in range(n_frames):
        if n_frames > 1:
            rho = rho_n[:, :, :, frame]
            print(f"=== FRAME {frame} ===")
        else:
            rho = rho_n

        # 2D data
        plane_data = compute_plane(rho, plane, mode)

        # Convert to ASCII
        ascii_lines = array_to_ascii(plane_data,
                                     width=args.width,
                                     height=args.height)

        # Add box
        boxed = add_box(ascii_lines)

        print(boxed)
        print("")


# ============================================================

if __name__ == "__main__":
    main()
