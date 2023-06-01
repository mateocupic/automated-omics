from Bio import motifs
import pandas as pd
import os
import re
from tqdm import tqdm
import re
import ensembl_rest
import requests
from Bio import pairwise2
from Bio.Align import substitution_matrices

def process_meme():
    files = os.listdir(data)
    genes["MEME"] = "+"
    for index, row in tqdm(genes.iterrows()):
        name = row['gene_short_name']
        regex = name + '.+'
        r = re.compile(regex)
        r2 = re.compile("error")
        seq = list(filter(r.match, files))

        try:
            with open(data + seq[0]) as file:
                fasta1 = '>' + str(seq[0]) + '\n'
                string = file.read().replace('\n', '')
                fasta1 = fasta1 + string

                if re.findall("error", fasta1):
                    genes.loc[genes['gene_short_name'] == name, 'MEME'] = 'Fasta {}'.format(seq[0])
        except:
            genes.loc[genes['gene_short_name'] == name, 'MEME'] = 'Fasta 1 or 2 missing'

        try:
            with open(data + seq[1]) as file:
                fasta2 = '>' + str(seq[1]) + '\n'
                string = file.read().replace('\n', '')
                fasta2 = fasta2 + string

                if re.findall("error", fasta2):
                    genes.loc[genes['gene_short_name'] == name, 'MEME'] = 'Fasta {}'.format(seq[1])
        except:
            genes.loc[genes['gene_short_name'] == name, 'MEME'] = 'Fasta 1 or 2 missing'

        fasta = fasta1 + '\n' + fasta2
        with open(output + "{}.txt".format(name), "w") as text_file:
            text_file.write(fasta)