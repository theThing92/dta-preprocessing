# Standard
import argparse
import random

# Pip
# None

# Custom
# None

__author__ = "Christopher Chandler"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="process items ",
        description="TBA",
    )

    parser.add_argument("unkk", "--unk", type=str, help="unk")
    args = parser.parse_args()
