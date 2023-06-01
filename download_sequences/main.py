import pandas as pd
from download_sequences import download_sequences
from parse_sequences import parse_sequences

def main():
    genes = pd.read_excel("path/to/deg sign.xlsx")
    genes['Downloaded'] = 0
    save_dir = "path/to/geni/"

    print("Downloading sequences...")
    download_sequences(genes, save_dir)
    genes.to_excel("path/to/deg sign_downloaded.xlsx")

    print("Parsing sequences...")
    parse_sequences(genes, save_dir)
    genes.to_excel("path/to/deg sign_parsed.xlsx")

if __name__ == "__main__":
    main()