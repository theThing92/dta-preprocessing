import glob
import os
import pickle

DATA_MISSING = "NA"


def extract_epochs(input_directory: str, output_file: str, as_pickle=False) -> dict:
    """
    Extract epoch information from the input pickle files (the output of Gruppe-1: Metadaten).

    Args:
        input_file (str): Name of the input file
        output_file (str): Name of the output file

    Returns:
        a txt file with epochs and text names
        +
        dict: Dictionary containing epoch information and corresponding filenames.
    """

    # Making an empty dictionary to store the information we want
    epoch_filename_list = {}

    # Using glob to get a list of .pkl files in the input directory
    pkl_files = glob.glob(input_directory)

    # Iterating over the .pkl files
    for file_path in pkl_files:
        with open(file_path, "rb") as f:
            xml_metadata = pickle.load(f)

        # Getting the value for the key 'pub_date':
        # If the key has no value, then data is missing
        pub_date = xml_metadata.get("pub_date", DATA_MISSING)
        # converting the string to int
        pub_date = int(pub_date)

        # classifying the pub_date to epochs:
        if pub_date in range(1700, 1750):
            epoch = 1
        # TODO: CHANGE BACK
        elif pub_date in range(1750, 1800):
            epoch = 2
        elif pub_date in range(1800, 1850):
            epoch = 3
        elif pub_date in range(1850, 1900):
            epoch = 4
        else:
            pass  # print (pub_date)
            epoch = "unclassified"

        # Adding information to the dictionary
        if epoch not in epoch_filename_list:
            epoch_filename_list[epoch] = []
        epoch_filename_list[epoch].append(
            os.path.splitext(os.path.basename(file_path))[0]
        )

    if as_pickle:
        with open(output_file.replace(".txt", ".pkl"), "wb") as pkl_file:
            from copy import deepcopy

            epoch_filename_list_copy = deepcopy(epoch_filename_list)
            # rename variables for further preprocessing
            try:
                epoch_filename_list_copy["E1"] = epoch_filename_list_copy.pop(1)
            except KeyError:
                pass
            try:
                epoch_filename_list_copy["E2"] = epoch_filename_list_copy.pop(2)
            except KeyError:
                pass
            try:
                epoch_filename_list_copy["E3"] = epoch_filename_list_copy.pop(3)
            except KeyError:
                pass
            try:
                epoch_filename_list_copy["E4"] = epoch_filename_list_copy.pop(4)
            except KeyError:
                pass
            try:
                epoch_filename_list_copy["E2_E4"] = (
                    epoch_filename_list_copy["E2"],
                    epoch_filename_list_copy["E4"],
                )
            except KeyError:
                pass
            pickle.dump(epoch_filename_list_copy, pkl_file)
    with open(output_file, "w") as txt_file:
        for epoch, filenames in epoch_filename_list.items():
            txt_file.write(f"Epoch: {epoch}, Text: {filenames}\n")

    return epoch_filename_list


# input_directory = input ('Please give your input directory: ')
# output_directory = input ('Please give your output direcotry')

# for file in input_directory:
#    input_file = file

# for out_file in output_directory:
#    output_file = out_file


# epochs_and_files = extract_epochs(input_file, output_file)

# Printing  the epoch and filename list
# for epoch, filenames in epochs_and_files.items():
#    print(f"Epoch: {epoch}, Text: {filenames}")
