import xml.etree.ElementTree as XMLTree
from typing import Dict, Any

def load_xml(path_to_xml_file: str) -> XMLTree:
    """TODO

    Args:
        path_to_xml_file:
    Return:
         tbd
    """
    return XMLTree.parse(path_to_xml_file)

def get_metadata(xml_tree: XMLTree.ElementTree) -> Dict[str, Any]:
    """TODO

    Args:
        path_to_xml_file:
    Return:
         tbd
    """
    # relevant information: tbd
    root: XMLTree.Element = xml_tree.getroot()


if __name__ == "__main__":
    xml_file_path: str = "dta_selection/brockes_vergnuegen03_1730.tcf.xml"
    xml_tree: XMLTree.ElementTree = load_xml(xml_file_path)
