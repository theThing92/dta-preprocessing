"""
Module to preprocess DTA corpus files via multiprocessing.
"""
import argparse
import logging
import multiprocessing as mp
import os
import sys

from preprocessing import run_meta_data_extraction

__author__ = "Maurice Vogel"


# basic logging
logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Multiprocess DTA data",
        description="Process DTA files in a given input directory and save the resulting"
        " output format into an given output directory.",
    )
    parser.add_argument(
        "input_directory", type=str, help="Directory path to the DTA input files."
    )
    parser.add_argument(
        "output_directory", type=str, help="Output directory path."
    )
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
            logging.info(log_msg_start.format(args.input_directory, args.num_processes))
        else:
            logging.info(log_msg_start.format(args.input_directory, os.cpu_count()))
        files = os.listdir(args.input_directory)
        file_paths = [
            os.path.abspath(os.path.join(args.input_directory, file_name))
            for file_name in files
        ]

        pool.starmap(
            run_meta_data_extraction,
            zip(file_paths, [args.output_directory for i in range(len(files))]),
        )
        logging.info(
            f"Preprocessing is finished. Files have been saved to {args.output_directory}."
        )
