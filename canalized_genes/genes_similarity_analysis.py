from tqdm import tqdm
import pandas as pd
import genes_similarity_analysis as gsa

def main():
    directory = './gene_sequence_dir/'
    gene_names = gsa.load_gene_names(directory)
    all_results = []
    for gene in tqdm(gene_names):
        all_results.extend(gsa.analyze_gene_similarity(gene, directory))
    result_df = pd.DataFrame(all_results)
    return result_df

if __name__ == "__main__":
    main()