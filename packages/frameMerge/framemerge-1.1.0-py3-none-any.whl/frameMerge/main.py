#!/usr/bin/env python3
import argparse

from .merger import Merger


def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge HDF5 frames with Hadamard encoding or rolling merge."
    )
    parser.add_argument("-f", "--file_name", required=True, help="Input HDF5 file")
    parser.add_argument(
        "-o", "--output_file", default="merged.h5", help="Output HDF5 file"
    )
    parser.add_argument(
        "--n_frames", type=int, default=10000, help="Number of frames to read"
    )
    parser.add_argument(
        "--n_merged_frames",
        type=int,
        default=3,
        help="Number of frames per block (Hadamard: must be prime and ≡ 3 mod 4)",
    )
    parser.add_argument(
        "--skip_pattern",
        type=str,
        default=None,
        help="Comma-separated indices to skip (rolling merge only)",
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["hadamard", "rolling"],
        default="hadamard",
        help="Merge type: 'hadamard' (proper encoding) or 'rolling' (simple merge)",
    )
    parser.add_argument(
        "--data_location", type=str, default="entry/data", help="HDF5 group path"
    )
    parser.add_argument("--data_name", type=str, default="data", help="Dataset name")
    parser.add_argument(
        "--n_workers", type=int, default=None, help="Number of parallel workers"
    )
    parser.add_argument(
        "--sequential", action="store_true", help="Run sequentially instead of parallel"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    skip_pattern = None
    if args.skip_pattern:
        skip_pattern = [int(x.strip()) for x in args.skip_pattern.split(",")]

    if args.type == "hadamard" and skip_pattern is not None:
        print("Warning: skip_pattern ignored for Hadamard encoding")
        skip_pattern = None

    merger = Merger(
        file_name=args.file_name,
        output_file=args.output_file,
        n_frames=args.n_frames,
        n_merged_frames=args.n_merged_frames,
        skip_pattern=skip_pattern,
        data_location=args.data_location,
        data_name=args.data_name,
        n_workers=args.n_workers,
        type=args.type,
    )

    merger.process(parallel=not args.sequential)


if __name__ == "__main__":
    main()
