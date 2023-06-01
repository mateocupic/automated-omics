from Bio import pairwise2, SeqIO, Align
import os
import pandas as pd
from typing import List
from collections import namedtuple

GenePair = namedtuple('GenePair', ['first_gene', 'second_gene', 'percent_similarity'])

def load_gene_names(directory: str) -> List[str]:
    gene_names = []
    for i in os.listdir(directory):
        gene_names.append(i.split('.txt')[0].split('_')[0])
    return list(set(gene_names))

def load_sequences_for_gene(gene: str, directory: str) -> List[SeqIO.SeqRecord]:
    fasta_files = [filename for filename in os.listdir(directory) if filename.startswith(gene)]
    return [SeqIO.read(f'{directory}/{fasta_name}', 'fasta') for fasta_name in fasta_files]

def analyze_gene_similarity(gene: str, directory: str) -> List[GenePair]:
    seqs = load_sequences_for_gene(gene, directory)
    results = []
    aligner = Align.PairwiseAligner()
    for i in range(1, len(seqs)):
        score = aligner.score(seqs[i].seq, seqs[i-1].seq)
        seq_length = min(len(seqs[i].seq), len(seqs[i-1].seq))
        percent_match = round((score / seq_length) * 100, 2)
        results.append(GenePair(fasta_files[i].split('.txt')[0], fasta_files[i-1].split('.txt')[0], percent_match))
    return results