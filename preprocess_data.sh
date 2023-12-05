#!/bin/bash
# please note that all directory strings have to end on backslash to be correctly parsable
# config number of cores for preprocessing here
export NUM_CORES=8
# input directories
export INPUT_DIR_XML="data/xml/"
export INPUT_DIR_PICKLE="data/pickle/"
export INPUT_DIR_CSV="data/csv/"
# output directories
export OUTPUT_DIR_ANNOTATIONS="data/test/"
export OUTPUT_DIR_META="data/test/"
export OUTPUT_DIR_EPOCHS="data/test/"
export OUTPUT_DIR_SENTENCES="data/test/"
export LEMMA="und"
# args process_documents.py input_directory output_directory function
python3 process_documents.py $INPUT_DIR_XML $OUTPUT_DIR_META meta -n $NUM_CORES
python3 process_documents.py $INPUT_DIR_XML $OUTPUT_DIR_ANNOTATIONS annotations -n $NUM_CORES
python3 process_documents.py $OUTPUT_DIR_META $OUTPUT_DIR_EPOCHS epochs -n $NUM_CORES
# TODO: only partial exectution possible
#python3 process_documents.py $INPUT_DIR_CSV $OUTPUT_DIR_SENTENCES sentences -l $LEMMA -n $NUM_CORES