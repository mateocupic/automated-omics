from Bio import Entrez
import re
import os

def parse_sequences(genes, save_dir):
    gene_names = list(genes['gene_short_name'])
    missing_data = open(os.path.join(save_dir, 'missing_protein.txt'), 'w')
    for gene in tqdm(gene_names, position=0, leave=True):
        try:
            parse_gene(gene, genes, save_dir)
        except:
            missing_data.write(gene + '\n')
    missing_data.close()

def parse_gene(gene, genes, save_dir):
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

            fetch = Entrez.efetch(db="nuccore", id=str(accession), rettype="gb", retmode='text',
                                  seq_start=chr_start, seq_stop=chr_end)
            record = fetch.read()
            seq = re.findall("\/translation=\"[^\"]+\"", record)

            for j in range(len(seq)):
                item = seq[j]
                item = re.sub(' +', '', item).strip()
                item = re.sub('\n+', '', item).strip()
                item = item.strip('/translation="')

                file_name = f"{gene}_{i}_prot{j}.txt"
                out_handle = open(os.path.join(save_dir, file_name), 'w')
                out_handle.write(item)
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

            fetch = Entrez.efetch(db="nuccore", id=str(accession), rettype="gb", retmode='text',
                                  seq_start=chr_start, seq_stop=chr_end)
            record = fetch.read()
            seq = re.findall("\/translation=\"[^\"]+\"", record)

            for j in range(len(seq)):
                item = seq[j]
                item = re.sub(' +', '', item).strip()
                item = re.sub('\n+', '', item).strip()
                item = item.strip('/translation="')

                file_name = f"{gene}_{i}_prot{j}.txt"
                out_handle = open(os.path.join(save_dir, file_name), 'w')
                out_handle.write(item)
                out_handle.close()