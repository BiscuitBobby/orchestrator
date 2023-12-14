# Get the SciQ dataset from HuggingFace
from datasets import load_dataset

dataset = load_dataset("sciq", split="train")

# Filter the dataset to only include questions with a support
dataset = dataset.filter(lambda x: x["support"] != "")

print("Number of questions with support: ", len(dataset))