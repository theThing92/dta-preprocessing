"""
Module to preprocess DTA corpus files via multiprocessing.
"""
import argparse
import multiprocessing as mp
import os
import pickle
import sys
from enum import Enum

from preprocessing import run_meta_data_extraction
from annotationen import get_annotations
from extract_epoch import extract_epochs
from processing_dta_file_choice import main_get_epoch_files
from item_generation import generate_items
from prob import fods_builder

__author__ = "Maurice Vogel"


class PreprocessingFunctions(Enum):
    annotations = "annotations"  # get_annotations
    epochs = "epochs"  # extract_epochs
    meta = "meta"  # run_meta_data_extraction
    docs_pairwise = "docs_pairwise"  # main_get_epoch_files
    sents_pairwise = "sents_pairwise"  # generate_items + fods_builder


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Multiprocess DTA data",
        description="Process DTA related files in a given input directory and save the resulting"
        " output format into a given output directory.",
    )
    parser.add_argument(
        "input_directory",
        type=str,
        help="Directory path to the DTA related input files.",
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
    parser.add_argument(
        "function",
        type=str,
        help=f"Preprocessing functions to call, can be one of:"
        f" {', '.join([x.value for x in PreprocessingFunctions])}",
        default=PreprocessingFunctions.meta.value,
    )
    parser.add_argument(
        "--items",
        "-i",
        type=str,
        help="Path to item list for extracting test items with sentence context"
        " in a given context window of n tokens (before and after).",
    )
    parser.add_argument(
        "--window_size",
        "-w",
        type=int,
        default=50,
        help="Window size of n tokens for context extraction (before and after).",
    )

    parser.add_argument(
        "--min_e2",
        type=int,
        default=15,
        help="Minimal number of items per target in epoch E2.",
    )

    parser.add_argument(
        "--min_e4",
        type=int,
        default=15,
        help="Minimal number of items per target in epoch E4.",
    )

    parser.add_argument(
        "--min_e2_e4",
        type=int,
        default=30,
        help="Minimal number of items per target in epoch E4.",
    )

    parser.add_argument(
        "--dir_csv_files", type=str, help="Path to directory with csv annotation files."
    )

    parser.add_argument(
        "--items_per_fod",
        type=int,
        default=5,
        help="Number of items to generate per fod file.",
    )

    args = parser.parse_args()

    with mp.Pool(processes=args.num_processes) as pool:
        log_msg_start = (
            "Start multiprocessing for DTA files in {} with {} processes and step '{}'."
        )
        if args.num_processes:
            print(
                log_msg_start.format(
                    args.input_directory, args.num_processes, args.function
                )
            )
        else:
            print(
                log_msg_start.format(
                    args.input_directory, os.cpu_count(), args.function
                )
            )
        files = os.listdir(args.input_directory)
        file_paths = [
            os.path.abspath(os.path.join(args.input_directory, file_name))
            for file_name in files
        ]

        if args.function == PreprocessingFunctions.meta.value:
            pool.starmap(
                run_meta_data_extraction,
                zip(file_paths, [args.output_directory for i in range(len(files))]),
            )

        elif args.function == PreprocessingFunctions.annotations.value:
            pool.starmap(
                get_annotations,
                zip(
                    file_paths,
                    [
                        os.path.join(
                            args.output_directory,
                            file.replace(".xml", ".csv").replace(".tcf", ""),
                        )
                        for file in files
                    ],
                ),
            )

        elif args.function == PreprocessingFunctions.epochs.value:
            extract_epochs(
                args.input_directory + "*.pkl",
                os.path.join(args.output_directory, "epochs.txt"),
                as_pickle=True,
            )

        elif args.function == PreprocessingFunctions.docs_pairwise.value:
            main_get_epoch_files(
                args.input_directory + "epochs.pkl", args.output_directory
            )

        elif args.function == PreprocessingFunctions.sents_pairwise.value:
            try:
                args.items
            except NameError:
                print("Please define a path to your items file.")
            try:
                args.window_size
            except NameError:
                print("Please define the context window extraction size.")
            try:
                args.min_e2
            except NameError:
                print("Please define the minimal target size for epoch E2.")
            try:
                args.min_e4
            except NameError:
                print("Please define the minimal target size for epoch E2.")
            try:
                args.min_e2_e4
            except NameError:
                print("Please define the minimal target size for epoch E2_E4.")
            try:
                args.items_per_fod
            except NameError:
                print("Please define the number of items per fod file.")

            with open(args.items, "r", encoding="utf-8") as f:
                items = f.readlines()
                items = [i.replace("\n", "") for i in items]

            with open(
                os.path.join(args.input_directory, "docs_pairwise.pkl"), "rb"
            ) as f:
                docs_pairwise = pickle.load(f)

            for k, item_list in docs_pairwise.items():
                for i, doc in enumerate(item_list):
                    docs_pairwise[k][i][0] = os.path.join(
                        args.dir_csv_files, doc[0] + ".csv"
                    )
                    docs_pairwise[k][i][1] = os.path.join(
                        args.dir_csv_files, doc[1] + ".csv"
                    )

            try:
                results_list = generate_items(
                    items,
                    docs_pairwise,
                    args.window_size,
                    args.min_e2,
                    args.min_e4,
                    args.min_e2_e4,
                )
                # flatten sentence pairs tuples (expected input for fods_builder)
                results_flattened = []
                for sentence_pair in results_list:
                    sent1 = sentence_pair[0]
                    sent2 = sentence_pair[1]
                    results_flattened.append(sent1)
                    results_flattened.append(sent2)

                path_output_pickle_sents_pairwise = os.path.join(
                    args.output_directory, "sents_pairwise.pkl"
                )
                with open(path_output_pickle_sents_pairwise, "wb") as f:
                    pickle.dump(results_flattened, f)
                fods_builder(
                    results_flattened, args.output_directory, args.items_per_fod
                )
            except Exception as e:
                print(e)
        else:
            raise ValueError(
                f"No valid function alias has been given, must be one of:"
                f" {', '.join([x.value for x in PreprocessingFunctions])}"
            )

    print(
        f"Preprocessing for step '{args.function}' is finished. Files have been saved to {args.output_directory}."
    )
