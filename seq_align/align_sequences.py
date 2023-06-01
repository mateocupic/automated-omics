import data_loading as dl
import aligner as sa


def main():
    gene_data = dl.load_gene_data("gene_data.xlsx")
    sequence_files = dl.load_sequence_data("sequences/")

    for sequence_file in sequence_files:
        sequence_data = dl.load_sequence_file(sequence_file)
        sequences = sa.parse_sequence_data(sequence_data)

        for seq1, seq2 in zip(sequences, sequences[1:]):
            alignment = sa.pairwise_alignment(seq1, seq2)
            return alignment

if __name__ == "__main__":
    main()