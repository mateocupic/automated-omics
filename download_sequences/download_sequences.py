import pandas as pd
from Bio import Entrez
from Bio import SeqIO
import time
from tqdm import tqdm
import re
import os

Entrez.email = "mateo.cupic@irb.hr"

def download_sequences(genes, save_dir):
    gene_names = list(genes['gene_short_name'])
    missing_data = open(os.path.join(save_dir, 'missing_data.txt'), 'w')
    for gene in tqdm(gene_names, position=0, leave=True):
        try:
            download_gene(gene, genes, save_dir)
            time.sleep(3)
        except:
            missing_data.write(gene + '\n')
    missing_data.close()

def download_gene(gene, genes, save_dir):
    if gene.startswith('ENSAM'):
        handle = Entrez.esearch(db="Gene", term=gene, rettype='gb', retmode='text')
        record = Entrez.read(handle)
        identifier = record['IdList']
        handle.close()

        summary = Entrez.esummary(db="Gene", id=identifier)
        record = Entrez.read(summary)
        summary.close()

        for i, entry in enumerate(record['DocumentSummarySet']['DocumentSummary'][0]['LocationHist']):
            accession = entry['ChrAccVer']
            chr_start = int(entry['ChrStart'])
            chr_end = int(entry['ChrStop'])

            fetch = Entrez.efetch(db="nuccore", id=str(accession), rettype="fasta", retmode='text')
            fasta = SeqIO.read(fetch, 'fasta')

            if chr_start < chr_end:
                fasta = fasta[chr_start:chr_end]
            else:
                fasta = fasta[chr_end:chr_start]
            fetch.close()

            if len(fasta.seq) > 0:
                genes.loc[genes['gene_short_name'] == gene, 'Downloaded'] += 1

            file_name = f"{gene}_{i}.txt"
            out_handle = open(os.path.join(save_dir, file_name), 'w')
            out_handle.write(fasta.format("fasta"))
            out_handle.close()

    else:
        handle = Entrez.esearch(db="Gene", term=f"Astyanax mexicanus[Orgn] AND {gene}[Gene]",
                                rettype='gb', retmode='text')
        record = Entrez.read(handle)
        identifier = record['IdList']
        handle.close()

        summary = Entrez.esummary(db="Gene", id=identifier)
        record = Entrez.read(summary)
        summary.close()

        for i, entry in enumerate(record['DocumentSummarySet']['DocumentSummary'][0]['LocationHist']):
            accession = entry['ChrAccVer']
            chr_start = int(entry['ChrStart'])
            chr_end = int(entry['ChrStop'])

            fetch = Entrez.efetch(db="nuccore", id=str(accession), rettype="fasta", retmode='text')
            fasta = SeqIO.read(fetch, 'fasta')

            if chr_start < chr_end:
                fasta = fasta[chr_start:chr_end]
            else:
                fasta = fasta[chr_end:chr_start]
            fetch.close()

            if len(fasta.seq) > 0:
                genes.loc[genes['gene_short_name'] == gene, 'Downloaded'] += 1

            file_name = f"{gene}_{i}.txt"
            out_handle = open(os.path.join(save_dir, file_name), 'w')
            out_handle.write(fasta.format("fasta"))
            out_handle.close()