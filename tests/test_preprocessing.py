# Standard
import glob
import unittest

# Custom
from preprocessing import run_meta_data_extraction

# Pip
# None


class TestXMLDataExtraction(unittest.TestCase):
    """
    A unit test class for XML data extraction.

    This class defines a set of test cases to ensure the proper extraction of metadata
    from DTA files located in the 'dta_selection' directory.
    """

    def test_dta_files(self) -> None:
        """
        Test the extraction of metadata from DTA files.

        This test case iterates through the list of DTA files and runs the
        'run_meta_data_extraction' function on each file to extract metadata.
        The test is successful if the data of every file can be extracted.
        """

        dta_files = glob.glob("data/xml/*")

        for row in dta_files:
            run_meta_data_extraction(row)


if __name__ == "__main__":
    pass
