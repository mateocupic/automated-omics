GENETIC_CODE = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
}

def is_synonymous(codon1, codon2):
    """
    Check if two codons are synonymous.
    """
    return GENETIC_CODE.get(codon1) == GENETIC_CODE.get(codon2)

def calculate_dn_ds(seq1, seq2):
    """
    Calculate the dN/dS ratio for two DNA sequences.
    """
    if len(seq1) != len(seq2) or len(seq1) % 3 != 0:
        raise ValueError("Sequences must be of equal length and divisible by 3")

    synonymous = 0
    nonsynonymous = 0

    for i in range(0, len(seq1), 3):
        codon1 = seq1[i:i+3]
        codon2 = seq2[i:i+3]
        if is_synonymous(codon1, codon2):
            synonymous += 1
        else:
            nonsynonymous += 1

    if synonymous == 0:
        return float('inf') # return infinity if no synonymous mutations to avoid division by zero
    return nonsynonymous / synonymous