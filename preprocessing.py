# Standard
import argparse
import os
import pickle
import xml.etree.ElementTree as ET

from typing import Dict, Any

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
    def xml_basic_data(xml_tag: str) -> list:
        """
        Extract data for a given XML tag.

        Args:
            xml_tag (str): The XML tag to extract data for.

        Returns:
            list: A list of extracted data.
        """
        tag_search = root.findall(f".//cmdp:{xml_tag}", xml_namespaces)
        tag_search_results = [tag_child.text for tag_child in tag_search]
        return tag_search_results

    # Author name data
    forename_results = root.findall(".//cmdp:forename", xml_namespaces)
    surename_results = root.findall(".//cmdp:surname", xml_namespaces)

    author_counter = 0
    for forename, surename in zip(forename_results, surename_results):
        root_data[f"author_{author_counter}"] = {
            "forename": forename.text,
            "surname": surename.text,
        }
        author_counter += 1

    # Publishing data
    pub_place = xml_basic_data("pubPlace")
    pub_date = xml_basic_data("date")
    pub_name = xml_basic_data("name")

    # Save publishing data
    root_data["pub_place"] = pub_place
    root_data["pub_date"] = pub_date
    root_data["pub_name"] = pub_name

    # Save Textclass data
    for child in root.findall(".//cmdp:classCode", xml_namespaces):
        scheme = child.get("scheme")
        scheme_data, scheme_text = scheme.split("#")[1], child.text
        root_data[scheme_data] = scheme_text

    return root_data


def save_metadata(
    xml_metadata: Dict[str, Any],
    output_dir: str = "xml_extracted_data",
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

    rel_file_name = split_file_elements[1]

    # Save data as pickle
    pickle_name = f"{output_dir}/{rel_file_name}.pkl"
    pickle.dump(xml_metadata, open(pickle_name, mode="wb"))

    # Save data as txt
    txt_results = list()
    for item in xml_metadata:
        if "author" in item:
            forename, surname = xml_metadata.get(item).values()
            author = f"{item}={forename}_{surname}"
            txt_results.append(author)

        else:
            if isinstance(xml_metadata.get(item), list):
                pub_date_data = "_".join(xml_metadata.get(item))
            else:
                pub_date_data = xml_metadata.get(item)
            data_point = f"{item}={pub_date_data}"
            txt_results.append(data_point)

    text_writer = open(f"{output_dir}/{rel_file_name}.txt", mode="w+", encoding="utf-8")

    # Create multiple rows each containing only three elements
    # so that the rows are not longer than 80 characters
    row = int(len(txt_results) / 3)
    row_end_counter = 3

    for i in range(row):
        row_start_counter = i * 3
        row_start, row_end = row_start_counter, row_end_counter
        row_results = txt_results[row_start:row_end]

        # Add '#' to each row so that it is read as a comment
        results = ",".join(row_results)
        txt = f"# {results} \n"
        text_writer.write(txt)

        row_end_counter += 3


def run_meta_data_extraction(xml_file_path):
    """
    Load an XML file, extract metadata, and save it to files.

    Args:
        xml_file_path (str): Path to the XML file to extract metadata from.

    Returns:
        None
    """
    xml_data: ET.ElementTree = load_xml(xml_file_path)
    xml_metadata = get_metadata(xml_data)
    save_metadata(xml_metadata, save_file_name=xml_file_path)


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

    args = parser.parse_args()

    # Extract data
    if args.extract_data:
        file_name = args.extract_data
        run_meta_data_extraction(file_name)
        print(f"The XML-data from {file_name} was extracted and saved.")

    # Show data, but do not save it
    if args.show_data:
        xml_tree: ET.ElementTree = load_xml(args.show_data)
        xml_meta_data = get_metadata(xml_tree)
        for data in xml_meta_data:
            print(data, xml_meta_data.get(data))