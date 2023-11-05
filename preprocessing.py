# Standard
import argparse
import logging
import os
import pickle
import xml.etree.ElementTree as ET
from enum import Enum
from typing import Any, Dict

# Pip
# None

# Custom
# None

"""
This program reads in an XML file from the DTA and extracts the necessary XML data from 
said file. The data is then saved as a .txt file and pickled dictionary. 
The following data points are saved: 

- Author: First name and last name
- Place of publication
- Publication date
- Publication name
- Text classifications (according to the XML tags specified in the resource directory)
"""


class MetaInformation(Enum):
    AUTHOR_SURNAME = "author_surname"
    AUTHOR_FORENAME = "author_forename"
    PUB_NAME = "pub_name"
    PUB_PLACE = "pub_place"
    PUB_DATE = "pub_date"


# Create a basic logger
logging.basicConfig(
    filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)


def load_xml(path_to_xml_file: str) -> ET.ElementTree:
    """
    Load an XML file and return an XML tree object.

    Args:
        path_to_xml_file (str): Path to the XML file to be loaded.

    Returns:
        ET.ElementTree: An XML tree object.
    """
    return ET.parse(path_to_xml_file)


def get_metadata(xml_tree_data: ET.ElementTree) -> Dict[str, Any]:
    """
    Extract metadata from an XML tree and return it as a dictionary.

    Args:
        xml_tree_data (ET.ElementTree): The XML tree to extract metadata from.

    Returns:
        Dict[str, Any]: A dictionary containing the extracted metadata.
    """
    # relevant information: cf. ressources/dta.txt
    root: ET.Element = xml_tree_data.getroot()
    root_data = dict()

    # Create XML-Namespaces
    xml_namespaces = {
        "cmd": "http://www.clarin.eu/cmd/1",
        "cmdp": "http://www.clarin.eu/cmd/1/profiles/clarin.eu:cr1:p_1381926654438",
    }

    # Extracting metadata
    # Author name data

    try:
        author_surname = root.find(
            ".//cmdp:author/cmdp:persName/cmdp:surname", xml_namespaces
        ).text
        author_forename = root.find(
            ".//cmdp:author/cmdp:persName/cmdp:forename", xml_namespaces
        ).text
        root_data[MetaInformation.AUTHOR_SURNAME.value] = author_surname
        root_data[MetaInformation.AUTHOR_FORENAME.value] = author_forename

    except AttributeError as e:
        logging.error(e)

    # Publishing data
    pub_place = root.find(
        ".//cmdp:sourceDesc/cmdp:biblFull/cmdp:publicationStmt/cmdp:pubPlace",
        xml_namespaces,
    ).text
    pub_date = root.find(
        ".//cmdp:sourceDesc/cmdp:biblFull/cmdp:publicationStmt/cmdp:date",
        xml_namespaces,
    ).text
    pub_name = root.find(".//cmdp:sourceDesc/cmdp:bibl", xml_namespaces).text

    # Save publishing data
    root_data[MetaInformation.PUB_PLACE.value] = pub_place
    root_data[MetaInformation.PUB_DATE.value] = pub_date
    root_data[MetaInformation.PUB_NAME.value] = pub_name

    # Save textClass data
    for child in root.findall(".//cmdp:classCode", xml_namespaces):
        scheme = child.get("scheme")
        scheme_data, scheme_text = scheme.split("#")[1], child.text
        if f"textClass_{scheme_data}" not in root_data.keys():
            root_data[f"textClass_{scheme_data}"] = scheme_text
        else:
            root_data[
                f"textClass_{scheme_data}"
            ] = f'{root_data[f"textClass_{scheme_data}"]},{scheme_text}'

    return root_data


def save_metadata(
    xml_metadata: Dict[str, Any],
    output_dir: str = ".",
    save_file_name: str = None,
) -> None:
    """
    Save metadata to a pickle and a text file.

    Args:
        xml_metadata (Dict[str, Any]): Dictionary with DTA meta information.
        output_dir (str): Path to the output directory to save metadata.
        save_file_name (str): The name for the saved metadata files.

    Returns:
        None
    """
    file, ext = os.path.splitext(save_file_name)
    delimiter = "/"
    if "/" not in os.path.splitext(file)[0]:
        delimiter = "\\"

    split_file_elements = os.path.splitext(file)[0].split(delimiter)

    rel_file_name = split_file_elements[-1]

    # Serialize data as pickle object
    pickle_name = f"{output_dir}/{rel_file_name}.pkl"
    pickle.dump(xml_metadata, open(pickle_name, mode="wb"))

    # Define output template strings for meta information
    string_author_surname = f"#{MetaInformation.AUTHOR_SURNAME.value}" + "={}"
    string_author_forename = f"#{MetaInformation.AUTHOR_FORENAME.value}" + "={}"
    string_pub_name = f"#{MetaInformation.PUB_NAME.value}" + "={}"
    string_pub_place = f"#{MetaInformation.PUB_PLACE.value}" + "={}"
    string_pub_date = f"#{MetaInformation.PUB_DATE.value}" + "={}"
    strings_text_class = []

    # Write meta data values as list items for ordering
    for key, value in xml_metadata.items():
        if key == MetaInformation.AUTHOR_SURNAME.value:
            string_author_surname = string_author_surname.format(value)
        elif key == MetaInformation.AUTHOR_FORENAME.value:
            string_author_forename = string_author_forename.format(value)
        elif key == MetaInformation.PUB_NAME.value:
            string_pub_name = string_pub_name.format(value)
        elif key == MetaInformation.PUB_PLACE.value:
            string_pub_place = string_pub_place.format(value)
        elif key == MetaInformation.PUB_DATE.value:
            string_pub_date = string_pub_date.format(value)
        else:
            strings_text_class.append(f"#{key}={value}")

    # Define output order for text file
    meta_data_out = [
        string_author_surname,
        string_author_forename,
        string_pub_name,
        string_pub_place,
        string_pub_date,
    ] + sorted(strings_text_class)

    # Write meta information to txt file

    with open(f"{output_dir}/{rel_file_name}.txt", "w") as f:
        for meta_datum in meta_data_out:
            print(meta_datum, file=f)


def run_meta_data_extraction(xml_file_path: str, output_directory: str):
    """
    Load an XML file, extract metadata, and save it to files.

    Args:
        output_directory (str): Name of the output directory for the .txt and pickle files
        xml_file_path (str): Path to the XML file to extract metadata from.

    Returns:
        None
    """
    xml_data: ET.ElementTree = load_xml(xml_file_path)
    xml_metadata = get_metadata(xml_data)

    save_metadata(
        xml_metadata=xml_metadata,
        output_dir=output_directory,
        save_file_name=xml_file_path,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="XML-DTA", description="Extract XML data from the file"
    )
    parser.add_argument(
        "-x", "--extract_data", type=str, help="Read in XML file and save data"
    )
    parser.add_argument(
        "-s", "--show_data", type=str, help="Read in XML file and show data"
    )
    parser.add_argument(
        "-o",
        "--output_directory",
        type=str,
        help="Name of the output directory for the .txt and pickle files",
    )
    args = parser.parse_args()
    # Extract data
    if args.extract_data:
        file_name = args.extract_data
        if args.output_directory:
            run_meta_data_extraction(file_name, args.output_directory)
            print(
                f"The XML-data from {file_name} was extracted and saved to {args.output_directory}."
            )
        else:
            run_meta_data_extraction(file_name, os.getcwd())
            print(
                f"The XML-data from {file_name} was extracted and saved in the "
                f"current working directory. "
            )
    # Show data, but do not save it
    if args.show_data:
        xml_tree: ET.ElementTree = load_xml(args.show_data)
        xml_meta_data = get_metadata(xml_tree)
        for data in xml_meta_data:
            print(data, xml_meta_data.get(data))
