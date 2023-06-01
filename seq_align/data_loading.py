import os
import pandas as pd

def load_gene_data(filepath):
    return pd.read_excel(filepath, header=None)

def load_sequence_data(directory):
    return [name for name in os.listdir(directory) if name.endswith(".txt")]

def load_sequence_file(filepath):
    with open(filepath) as file:
        return file.read().replace('\n', '')