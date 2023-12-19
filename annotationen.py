import csv
import xml.etree.ElementTree as ET


def get_annotations(file, newfilename):
    """Function that extracts the annotation-features from the xml-files
    Input:  file: xml-file with the texts
            newfilename: filename for the annotations-file
    Output: table with the features as a annotations-file
    """

    # parse the file with Elementtree and get the root
    tree = ET.parse(file)
    root = tree.getroot()

    # Define the namespace
    namespace = {"ns": "http://www.dspin.de/data/textcorpus"}

    # Find the 'token' elements
    token_elements = root.findall(".//ns:token", namespaces=namespace)

    tok_dict = dict()
    # retrieve the token IDs and the tokens
    for token_element in token_elements:
        token_id = token_element.get("ID")
        token_text = token_element.text
        # tok_dict: key = token ID, value = list with token_text
        tok_dict[token_id] = [token_text]

    # Find the 'sentence' elements
    sentence_elements = root.findall(".//ns:sentence", namespaces=namespace)

    sent_dict = dict()
    # retrieve the sentence IDs and the sentence structures
    for sentence_element in sentence_elements:
        sentence_id = sentence_element.get("ID")
        sentence_text = sentence_element.get("tokenIDs")
        sent_dict[sentence_id] = sentence_text
    # print(sent_dict)

    # Find the 'lemma' elements
    lemma_elements = root.findall(".//ns:lemma", namespaces=namespace)

    for lemma_element in lemma_elements:
        lemma_id = lemma_element.get("tokenIDs")
        lemma_text = lemma_element.text
        # proof if lemma ID in tok_dict as a key to save the lemma_text
        # append the lemma to the value list
        if lemma_id in tok_dict.keys():
            tok_dict[lemma_id].append(lemma_text)

    # Find the 'POS' elements
    pos_elements = root.findall(".//ns:tag", namespaces=namespace)

    for pos_element in pos_elements:
        pos_id = pos_element.get("tokenIDs")
        pos_text = pos_element.text
        # proof if pos ID in tok_dict as a key to save the pos tags
        # append the tags to the value list
        if pos_id in tok_dict.keys():
            tok_dict[pos_id].append(pos_text)

    # Find the 'correction' elements
    corr_elements = root.findall(".//ns:correction", namespaces=namespace)

    for corr_element in corr_elements:
        corr_id = corr_element.get("tokenIDs")
        corr_text = corr_element.text
        # proof if corr ID in tok_dict as a key to save the corr tokens
        # append the corr tokens to the value list
        if corr_id in tok_dict.keys():
            tok_dict[corr_id].append(corr_text)

    # append the original token if there is no corrected token
    for entry in tok_dict:
        if len(tok_dict[entry]) != 4:
            tok_dict[entry].append(tok_dict[entry][0])

    # structure of the dictionarys:
    # for corrected tokens: key = token_ID, value = [orig_token, lemma, POS_tag, corr_token]
    # for the others: key = token_ID, value = [orig_token, lemma, POS_tag, orig_token]

    # Creating a mapping from token IDs to their respective sentence IDs
    token_sentence_mapping = {}
    for entry in sent_dict:
        sent_list = sent_dict[entry].split()
        for element in sent_list:
            if element in tok_dict:
                if element in token_sentence_mapping:
                    token_sentence_mapping[element].append(entry)
                else:
                    token_sentence_mapping[element] = [entry]
            else:
                print("Element not in tok_dict")

    # Idea coming from chat.openai.com, sollution adapted.
    # Writing to CSV using DictWriter for more structured handling
    fieldnames = ["Sent_ID", "Token_ID", "Corr_token", "Orig_token", "Lemma", "POS"]

    with open(newfilename, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        # Writing rows to the CSV file
        for key, values in tok_dict.items():
            sentence_ids = token_sentence_mapping.get(key, [""])
            row = {
                "Sent_ID": sentence_ids[0],  # Consider first sentence ID
                "Token_ID": key,
                "Corr_token": values[3],
                "Orig_token": values[0],
                "Lemma": values[1],
                "POS": values[2],
            }
            writer.writerow(row)

    # reformat output dict to conform with expected input format of group 3

    # return csv_file


# Run the function with the first file of the dta_selection
# datafile = input("Dateipfad der xml-Datei angeben: ")
# C:\Users\Noemi\Documents\Unizeugs\Linguistik\Semantischer_Wandel\dta_selection\dta_selection\brockes_vergnuegen03_1730.tcf.xml
# filename = input("Name der annotations-Datei mit .annotations: ")
# brockes_vergnuegen03.annotations
# get_annotations(datafile, filename)
