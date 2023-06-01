import pandas as pd
from Bio import Entrez
from tqdm import tqdm

def load_data(deseq_path, transcriptome_path, trinotate_path):
    deseq= pd.read_excel(deseq_path)
    target_organism_transcriptome = pd.read_excel(transcriptome_path)
    trinotate = pd.read_excel(trinotate_path)
    return deseq, target_organism_transcriptome, trinotate

def merge_data(df_merged, trinotate):

    # Combine 'sampleA' and 'sampleB' columns into a single 'sample' column
    df_merged['sample'] = df_merged['sampleA'] + '-' + df_merged['sampleB']

    # Drop unnecessary columns
    df_merged.drop(columns=['sampleA', 'sampleB'], inplace=True)

    # Clean up the 'sprot_Top_BLASTX_hit' column in the 'trinotate' dataframe
    trinotate['sprot_Top_BLASTX_hit'] = trinotate['sprot_Top_BLASTX_hit'].str.split('^').str[0]
    trinotate = trinotate[['#gene_id', 'transcript_id', 'sprot_Top_BLASTX_hit', 'gene_ontology_Pfam']]
    trinotate = trinotate.drop_duplicates()

    # Merge the 'trinotate' dataframe with the 'df_merged' dataframe
    df_merged = df_merged.merge(trinotate, how='left', on='transcript_id')
    return df_merged

def fetch_protein_titles(df_merged):
    # Configure Entrez email
    Entrez.email = "mateo.cupic@irb.hr"

    # Initialize the list to store protein titles
    titles = []

    # Fetch protein titles for each accession
    for accession in tqdm(df_merged['sprot_Top_BLASTX_hit']):
        try:
            handle = Entrez.esummary(db="protein", id=accession)
            record = Entrez.read(handle)
            if len(record) > 1:
                print('Multiple records')
                break
            titles.append(record[0]['Title'])
        except:
            titles.append('Entry not found')

    # Add the protein titles to the 'df_merged' dataframe
    df_merged['protein'] = titles
    return df_merged

def process_gene_ontology(df_merged):
    # Split the 'gene_ontology_Pfam' column into separate columns
    df_merged['gene_ontology_Pfam'] = df_merged['gene_ontology_Pfam'].str.split('`').tolist()
    df_merged = df_merged.explode('gene_ontology_Pfam')
    df_merged['go_term'] = df_merged['gene_ontology_Pfam'].str.split('^').str[0]
    df_merged['go_prefix'] = df_merged['gene_ontology_Pfam'].str.split('^', 1).str[1]
    return df_merged

def save_merged_data(df_merged):
    # Save the merged dataframe to an Excel file
    df_merged.to_excel('deseq_merged_trinotate.xlsx')

def merge_with_target_organism_transcriptome(df_merged, target_organism_transcriptome):
    # Rename columns in the 'target_organism_transcriptome' dataframe
    target_organism_transcriptome.rename(columns={
        'log2FoldChange': 'log2FoldChange_target',
        'gene_ontology_Pfam': 'go_pfam_target',
        'padj': 'padj_target',
        'gene_ontology_prefix': 'go_ontology_prefix_target',
        'sprot_Top_BLASTX_hit': 'sprot_Top_BLASTX_hit_target',
        'Gene': 'gene_target',
    }, inplace=True)

    # Merge the 'target_organism_transcriptome' dataframe with the 'df_merged' dataframe
    df_merged_target = df_merged.merge(target_organism_transcriptome, how='left', on='transcript_id', indicator=True).drop_duplicates()

    # Filter rows with matching entries in both dataframes
    df_merged_target = df_merged_target.loc[df_merged_target['_merge'] == 'both']

    # Save the merged dataframe to an Excel file
    df_merged_target.drop_duplicates().to_excel('deseq_merged_target.xlsx')
