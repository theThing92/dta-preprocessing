import pickle
from prob import fods_builder

PATH_TO_SENTS_PAIRWISE_PKL = "data/test/sents_pariwise.pkl"
OUTPUT_PATH_FOS = "./"
NUM_ITEMS_PER_FILE = 5

# load data
with open(PATH_TO_SENTS_PAIRWISE_PKL, "rb") as f:
    data = pickle.load(f)

fods_builder(data, output_dir=OUTPUT_PATH_FOS, pairs_per_file=NUM_ITEMS_PER_FILE)