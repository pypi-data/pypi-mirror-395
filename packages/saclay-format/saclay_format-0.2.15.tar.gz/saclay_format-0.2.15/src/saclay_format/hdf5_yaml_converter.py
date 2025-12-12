#!/usr/bin/env python3
import os
import sys
import argparse

try:
    import saclay_format as saclay_parser
except ImportError:
    import saclay_parser


def convert_to_hdf5(header_path):
    """
    Convert from YAML+binary format -> HDF5.
    Example:
        python3 trans_hdf5_yml.py test.yaml -hdf5
    """
    if not os.path.exists(header_path):
        print(f"Error: YAML file not found: {header_path}")
        sys.exit(1)

    data = saclay_parser.read(header_path)

    # Set output file
    prefix = os.path.splitext(os.path.basename(header_path))[0]
    output_path = os.path.join(os.path.dirname(header_path) or ".", prefix + ".h5")

    # Update prefix in metadata to match filename
    data["metadata"]["prefix"] = prefix

    saclay_parser.write(data, output_path)
    print(f"Converted {header_path} -> {output_path}")


def convert_to_yml(h5_path):
    """
    Convert from HDF5 -> YAML+binary format.
    Example:
        python3 trans_hdf5_yml.py test.h5 -yml
    """
    if not os.path.exists(h5_path):
        print(f"Error: HDF5 file not found: {h5_path}")
        sys.exit(1)

    data = saclay_parser.read(h5_path)

    # Set output file
    prefix = os.path.splitext(os.path.basename(h5_path))[0]
    output_path = os.path.join(os.path.dirname(h5_path) or ".", prefix + ".yaml")

    # Update prefix in metadata to match filename
    data["metadata"]["prefix"] = prefix

    saclay_parser.write(data, output_path)
    print(f"Converted {h5_path} -> {output_path} and binary field files")


def main():
    parser = argparse.ArgumentParser(
        description="Convert between custom binary/YAML format and HDF5 format for Bogoliubov data."
    )
    parser.add_argument("input", help="Input file (.yaml/.yml or .h5/.hdf5)")

    parser.add_argument(
        "-hdf5", "-h5",
        action="store_true",
        dest="hdf5",
        help="Convert YAML+binary -> HDF5"
    )
    parser.add_argument(
        "-yml", "-yaml",
        action="store_true",
        dest="yml",
        help="Convert HDF5 -> YAML+binary"
    )
    args = parser.parse_args()

    if args.hdf5 and args.yml:
        print("Error: Please specify only one of -hdf5/-h5 or -yml/-yaml.")
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    # Auto mode: infer conversion direction if no flag is given
    if not args.hdf5 and not args.yml:
        if args.input.endswith(('.yaml', '.yml')):
            args.hdf5 = True
        elif args.input.endswith(('.h5', '.hdf5')):
            args.yml = True
        else:
            print("Error: Unrecognized file type. Use -hdf5/-h5 or -yml/-yaml explicitly.")
            sys.exit(1)

    if args.hdf5:
        convert_to_hdf5(args.input)
    elif args.yml:
        convert_to_yml(args.input)


if __name__ == "__main__":
    main()
