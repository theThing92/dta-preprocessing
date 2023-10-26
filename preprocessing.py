import xml.etree.ElementTree as XMLTree
from typing import Dict, Any

def load_xml(path_to_xml_file: str) -> XMLTree:
    """TODO

    Args:
        path_to_xml_file:
    Returns:
         An xml tree object.
    """
    return XMLTree.parse(path_to_xml_file)

def get_metadata(xml_tree: XMLTree.ElementTree) -> Dict[str, Any]:
    """TODO

    Args:
        path_to_xml_file:
    Returns:
         tbd
    """
    # relevant information: cf. ressources/dta.txt
    root: XMLTree.Element = xml_tree.getroot()

def save_metadata(dict_metadata: Dict[str, Any], output_dir: str) -> None:
    """TODO

        Args:
            dict_metadata: Dictionary with DTA meta information.
            output_dir: Path to output directory to save meta data as "csv header".
        Returns:
             None
    """

if __name__ == "__main__":
    xml_file_path: str = "data/xml/brockes_vergnuegen03_1730.tcf.xml"
    xml_tree: XMLTree.ElementTree = load_xml(xml_file_path)
