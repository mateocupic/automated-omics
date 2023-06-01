import pandas as pd
from Bio import Entrez
from tqdm import tqdm

class DataAnalysisHelper:
    def __init__(self):
        self.deseq = None
        self.target_organism_transcriptome = None
        self.trinotate = None

    def load_data(self, deseq_path, transcriptome_path, trinotate_path):
        self.deseq = pd.read_excel(deseq_path)
        self.target_organism_transcriptome = pd.read_excel(transcriptome_path)
        self.trinotate = pd.read_excel(trinotate_path)

    def merge_data(self):
        # Combine 'sampleA' and 'sampleB' columns into a single 'sample' column
        self.deseq['sample'] = self.deseq['sampleA'] + '-' + self.deseq['sampleB']

        # Drop unnecessary columns
        self.deseq.drop(columns=['sampleA', 'sampleB'], inplace=True)

        # Clean up the 'sprot_Top_BLASTX_hit' column in the 'trinotate' dataframe
        self.trinotate['sprot_Top_BLASTX_hit'] = self.trinotate['sprot_Top_BLASTX_hit'].str.split('^').str[0]
        self.trinotate = self.trinotate[['#gene_id', 'transcript_id', 'sprot_Top_BLASTX_hit', 'gene_ontology_Pfam']]
        self.trinotate = self.trinotate.drop_duplicates()

        # Merge the 'trinotate' dataframe with the 'deseq' dataframe
        self.deseq = self.deseq.merge(self.trinotate, how='left', on='transcript_id')

    def fetch_protein_titles(self):
        # Configure Entrez email
        Entrez.email = "your_email@example.com"

        # Initialize the list to store protein titles
        titles = []

        # Fetch protein titles for each accession
        for accession in tqdm(self.deseq['sprot_Top_BLASTX_hit']):
            try:
                handle = Entrez.esummary(db="protein", id=accession)
                record = Entrez.read(handle)
                if len(record) > 1:
                    print('Multiple records')
                    break
                titles.append(record[0]['Title'])
            except:
                titles.append('Entry not found')

        # Add the protein titles to the 'deseq' dataframe
        self.deseq['protein'] = titles

    def process_gene_ontology(self):
        # Split the 'gene_ontology_Pfam' column into separate columns
        self.deseq['gene_ontology_Pfam'] = self.deseq['gene_ontology_Pfam'].str.split('`').tolist()
        self.deseq = self.deseq.explode('gene_ontology_Pfam')
        self.deseq['go_term'] = self.deseq['gene_ontology_Pfam'].str.split('^').str[0]
        self.deseq['go_prefix'] = self.deseq['gene_ontology_Pfam'].str.split('^', 1).str[1]

    def save_merged_data(self, output_path):
        # Save the merged dataframe to an Excel file
        self.deseq.to_excel(output_path)

    def merge_with_target_organism_transcriptome(self):
        # Rename columns in the 'target_organism_transcriptome' dataframe
        self.target_organism_transcriptome.rename(columns={
            'log2FoldChange': 'log2FoldChange_target',
            'gene_ontology_Pfam': 'go_pfam_target',
            'padj': 'padj_target',
            'gene_ontology_prefix': 'go_ontology_prefix_target',
            'sprot_Top_BLASTX_hit': 'sprot_Top_BLASTX_hit_target',
            'Gene': 'gene_target',
        }, inplace=True)

        # Merge the 'target_organism_transcriptome' dataframe with the 'deseq' dataframe
        df_merged_target = self.deseq.merge(self.target_organism_transcriptome, how='left', on='transcript_id', indicator=True).drop_duplicates()

        # Filter rows with matching entries in both dataframes
        df_merged_target = df_merged_target.loc[df_merged_target['_merge'] == 'both']

        # Save the merged dataframe to an Excel file
        df_merged_target.drop_duplicates().to_excel('deseq_merged_target.xlsx')

    def perform_analysis(self):
        self.merge_data()
        self.fetch_protein_titles()
        self.process_gene_ontology()
        self.save_merged_data('deseq_merged_trinotate.xlsx')
        self.merge_with_target_organism_transcriptome()

    def run(self, deseq_path, transcriptome_path, trinotate_path):
        self.load_data(deseq_path, transcriptome_path, trinotate_path)
        self.perform_analysis()