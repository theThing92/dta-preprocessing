"""
Module to preprocess DTA corpus files via multiprocessing.
"""
# Standard
import argparse
import multiprocessing as mp
import os
import sys

# Custom
from preprocessing import run_meta_data_extraction
from logger.basic_logger import log_output

__author__ = "Maurice Vogel"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Multiprocess DTA data",
        description="Process DTA files in a given input directory and save the resulting"
        " output format into an given output directory.",
    )
    parser.add_argument(
        "input_directory", type=str, help="Directory path to the DTA input files."
    )
    parser.add_argument("output_directory", type=str, help="Output directory path.")
    parser.add_argument(
        "-n",
        "--num_processes",
        default=None,
        required=False,
        type=int,
        help="Number of processes to spawn for preprocessing functions."
        " Uses all available logical cpus per default, as returned from os.cpu_count().",
    )
    args = parser.parse_args()

    with mp.Pool(processes=args.num_processes) as pool:
        log_msg_start = "Start multiprocessing for DTA files in {} with {} processes."
        if args.num_processes:
            log_output(log_msg_start.format(args.input_directory, args.num_processes))
        else:
            log_output(log_msg_start.format(args.input_directory, os.cpu_count()))
        files = os.listdir(args.input_directory)
        file_paths = [
            os.path.abspath(os.path.join(args.input_directory, file_name))
            for file_name in files
        ]

        pool.starmap(
            run_meta_data_extraction,
            zip(file_paths, [args.output_directory for i in range(len(files))]),
        )
        log_output(
            f"Preprocessing is finished. Files have been saved to {args.output_directory}."
        )
