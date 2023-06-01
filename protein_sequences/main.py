from protein_sequences.common_substring import longest_common_substring
from protein_sequences.meme import process_meme
from protein_sequences.pairwise_alignment import pairwise_alignment


def main():
    sequences = "./input_sequence_dir"

    print("Running MEME algorithm...")
    process_meme(sequences)

    print("Running Pairwise alignment...")
    pairwise_alignment(sequences)

    print("Finding longest common substring...")
    longest_common_substring(sequences)


if __name__ == "__main__":
    main()