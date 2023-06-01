from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from Bio import SeqIO

def pairwise_alignment(file):
    sequences = [record.seq for record in SeqIO.parse(file, "fasta")]
    alignments = pairwise2.align.globalxx(sequences[0], sequences[1])

    # print the alignments
    for alignment in alignments:
        print(format_alignment(*alignment))