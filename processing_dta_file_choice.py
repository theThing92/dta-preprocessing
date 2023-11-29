# Standard
import random

# Custom
from sem_change.Annotationen import get_annotations

__author__ = "Christopher Chandler"

# So that all the results are the same on each system
seed_value = 42
random.seed(seed_value)


# This is dummy data for the epoch information that is to be supplied at a later data.
# It simply fills the respect lists with sample files.
epoch_data = {
    "E2": list(),
    "E4": list(),
}

for i in range(1, 1001):
    epoch_data["E2"].append(f"E2_file_{i}")
    epoch_data["E4"].append(f"E4_file_{i}")

epoch_data["E2_E4"] = epoch_data["E2"] , epoch_data["E4"]


def get_unique_epoch_files(epoch: str) -> dict:
    """

    """
    dta_files = list(epoch_data.get(epoch))

    file_groups = list()
    used = list()

    for i in range(1000):
        rand_choice = random.sample(dta_files, 2)
        taken = all([i in used for i in rand_choice])
        if not taken:
            file_groups.append(rand_choice)
            used.extend(rand_choice)

    file_groups.sort()

    return file_groups


def get_mixed_epoch_files(epoch: str) -> dict:
    """ """
    dta_files = list(epoch_data.get(epoch))

    file_groups = list()
    used = list()

    for i in range(2000):
        rand_choice_E2 = random.sample(dta_files[0], 1)
        rand_choice_E4 = random.sample(dta_files[1], 1)

        if rand_choice_E4 not in used and rand_choice_E2 not in used:
            file_groups.append((rand_choice_E2+rand_choice_E4))

        used.append(rand_choice_E2)
        used.append(rand_choice_E4)


    file_groups.sort()




    return file_groups


def main_get_epoch_files():

    epoch_2 = get_unique_epoch_files("E2")
    epoch_4 = get_unique_epoch_files("E4")
    epoch_2_4 = get_mixed_epoch_files("E2_E4")

    data = {"E2": epoch_2, "E4": epoch_4, "E2_E4": epoch_2_4}

    for i in data.get("E2_E4"):
        print(i)


    return data


if __name__ == "__main__":
    main_get_epoch_files()
