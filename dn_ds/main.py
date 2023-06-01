import sequence_processing as sp
import codon_analysis as ca

def main():
    seq1 = sp.read_seq_from_file("seq1.txt")
    seq2 = sp.read_seq_from_file("seq2.txt")

    distance = sp.hamming_distance(seq1, seq2)
    print(f"Hamming distance: {distance}")

    for i in range(0, len(seq1), 3):
        codon1 = seq1[i:i+3]
        codon2 = seq2[i:i+3]
        if not ca.is_synonymous(codon1, codon2):
            print(f"Non-synonymous mutation: {codon1} -> {codon2}")

    dn_ds_ratio = ca.calculate_dn_ds(seq1, seq2)
    print(f"dN/dS ratio: {dn_ds_ratio}")

if __name__ == "__main__":
    main()