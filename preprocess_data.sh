#!/bin/bash
# install progressbar for items (optional, can be uncommented, cf. README.md)
python3 -m pip install tqdm
# install pandas for faster csv data processing (**REQUIRED**)
python3 -m pip install pandas
# please note that all directory strings have to end on a backslash to be correctly parsable
# config number of cores for preprocessing here
NUM_CORES=8
# define input directories here
INPUT_DIR_XML="data/xml/"
# define output directories here
OUTPUT_DIR_ANNOTATIONS="data/test/annotations/"
OUTPUT_DIR_META="data/test/meta/"
OUTPUT_DIR_EPOCHS="data/test/epochs/"
OUTPUT_DIR_DOCS_PAIRWISE="data/test/docs_pairwise/"
OUTPUT_DIR_FODS="data/test/fods/"
# create output directories
mkdir -p $OUTPUT_DIR_ANNOTATIONS
mkdir -p $OUTPUT_DIR_META
mkdir -p $OUTPUT_DIR_EPOCHS
mkdir -p $OUTPUT_DIR_DOCS_PAIRWISE
mkdir -p $OUTPUT_DIR_FODS
# path to item file (one item per line, no newline at end of file)
ITEMS="data/items/items.txt"
# window size for context extraction
WINDOW_SIZE=50
# minimum number of items per target and epoch
MIN_ITEMS_E2=15 # default: 15
MIN_ITEMS_E4=15 # default: 15
MIN_ITEMS_E2_E4=30 # default: 30
# number of items per fod file
NUM_ITEMS_PER_FOD=5 # default: 5

# args process_documents.py input_directory output_directory function
# execute preprocessing pipeline
# step 1: extract meta information from xml files
python3 process_documents.py $INPUT_DIR_XML $OUTPUT_DIR_META meta -n $NUM_CORES
# step 2: generate csv dta files from xml files
python3 process_documents.py $INPUT_DIR_XML $OUTPUT_DIR_ANNOTATIONS annotations -n $NUM_CORES
# step 3: generate epoch lookup hashmap for corpus files according to meta information
python3 process_documents.py $OUTPUT_DIR_META $OUTPUT_DIR_EPOCHS epochs -n $NUM_CORES
# step 4: generate documents pairs for epochs E2, E4 and E2+E4
python3 process_documents.py $OUTPUT_DIR_EPOCHS $OUTPUT_DIR_DOCS_PAIRWISE docs_pairwise -n $NUM_CORES
# step 5: generate test item sentence pairs and write them into fod files
python3 process_documents.py $OUTPUT_DIR_DOCS_PAIRWISE $OUTPUT_DIR_FODS sents_pairwise -i $ITEMS -w $WINDOW_SIZE -n $NUM_CORES --min_e2 $MIN_ITEMS_E2 --min_e4 $MIN_ITEMS_E4 --min_e2_e4 $MIN_ITEMS_E2_E4 --dir_csv_files $OUTPUT_DIR_ANNOTATIONS --items_per_fod $NUM_ITEMS_PER_FOD