def read_seq_from_file(file_path):
    """
    Read gene sequences from a text file.
    """
    with open(file_path, "r") as file:
        sequence = file.read().replace("\n", "")
    return sequence

def hamming_distance(seq1, seq2):
    """
    Calculate the Hamming distance between two DNA sequences.
    """
    if len(seq1) != len(seq2):
        raise ValueError("Sequences must be of equal length")
    return sum(el1 != el2 for el1, el2 in zip(seq1, seq2))