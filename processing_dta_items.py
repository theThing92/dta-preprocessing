# Standard
import random

# Custom
from sem_change.Annotationen import get_annotations

__author__ = "Christopher Chandler"

# So that all the results are the same on each system
seed_value = 42
random.seed(seed_value)

# This is dummy data for the epoch information that is to be supplied at a later data.
epoch_data = {
    "E2": [
        "data/xml/brockes_vergnuegen03_1730.tcf.xml",
        "data/xml/dannhauer_catechismus04_1653.tcf.xml",
        "data/xml/hundtradowsky_judenschule01_1822.tcf.xml",
    ],
    "E4": [
        "data/xml/mohl_staatswissenschaften_1859.tcf.xml",
        "data/xml/mommsen_roemische03_1856.tcf.xml",
        "data/xml/paul_flegeljahre03_1804.tcf.xml",
    ],
}


def get_epoch_sentences(epoch: str) -> dict:
    """
    Get randomly selected sentences for a given epoch.

    Args:
        epoch (str): The epoch identifier.

    Returns:
        dict: A dictionary containing file names as keys and lists of
        randomly selected sentences as values.
    """
    dta_files = list(epoch_data.get(epoch))
    rand_choice = random.sample(dta_files, 2)

    epoch_choice = dict()
    for choice in rand_choice:
        epoch_choice[choice] = list()

    for file in rand_choice:
        sentence_annotations = get_annotations(
            file=file,
            newfilename="processing_results/extracted_sentences/test.csv",
        )
        epoch_choice[file].append(sentence_annotations)

    return epoch_choice


def get_sentence_data(epoch_dataset: dict, sentence_amount: int = 500) -> dict:
    """
    Generate random sentences for a given epoch dataset.

    Args:
        epoch_dataset (dict): The dictionary containing files and their associated sentences.
        sentence_amount (int): The number of sentences to be sampled.

    Returns:
        dict: A dictionary containing file names as keys and lists of randomly extracted sentences as values.
    """
    epoch_joined_sentences = dict()
    randomly_extracted_sentences = list()

    epoch_choice = dict()
    for choice in epoch_dataset:
        epoch_choice[choice] = list()

    # Iterate over each file
    for file in epoch_dataset:
        # Iterate over each dataset per file
        for data_point in epoch_dataset.get(file):
            # Iterate over each data point in the dataset
            for sen in data_point:
                # Sentence information for rebuilding the sentence
                sent_id = sen.get("Sent_ID")
                orig_token = sen.get("Orig_token")

                # create data entry and append them to the respective lists
                if epoch_joined_sentences.get(sent_id, None) is None:
                    epoch_joined_sentences[sen.get("Sent_ID")] = list()
                else:
                    epoch_joined_sentences[sen.get("Sent_ID")].append(orig_token)

            epoch_sentence_key_id = list(epoch_joined_sentences.keys())
            rand_sen_choice = random.sample(epoch_sentence_key_id, sentence_amount)

            # Join the sentence and append them to their respective file
            # Then empty the list so that the next file can be appended.
            for rand_sen in rand_sen_choice:
                joined_sentence = " ".join(epoch_joined_sentences.get(rand_sen))
                randomly_extracted_sentences.append(joined_sentence)
            epoch_choice[file] = randomly_extracted_sentences

            # Empty list
            randomly_extracted_sentences = list()

    return epoch_choice


def main_generate_sentences() -> tuple(dict[str, list], dict[str, list]):
    """
    Main function to generate sentences for epochs.

    Returns:
        tuple: A tuple containing two dictionaries, one for each epoch,
        with file names as keys and lists of randomly extracted sentences as values.
    """
    epoch_2 = get_epoch_sentences("E2")
    epoch_4 = get_epoch_sentences("E4")

    epoch_2_sentence_data = get_sentence_data(epoch_2)
    epoch_4_sentence_data = get_sentence_data(epoch_4)

    return epoch_2_sentence_data, epoch_4_sentence_data


if __name__ == "__main__":
    main_generate_sentences()
