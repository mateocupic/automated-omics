from deseq2_analysis import load_data, merge_data, fetch_protein_titles, process_gene_ontology, save_merged_data, merge_with_target_organism_transcriptome

if __name__ == "__main__":
    deseq_path = ''
    transcriptome_path = ''
    trinotate_path = ''

    # Load data
    deseq, target_organism_transcriptome, trinotate = load_data(deseq_path, transcriptome_path, trinotate_path)

    # Merge DESeq2 data with Trinotate data
    merged_data = merge_data(deseq, trinotate)

    # Fetch protein titles
    merged_data = fetch_protein_titles(merged_data)

    # Process gene ontology
    merged_data = process_gene_ontology(merged_data)

    # Save merged data
    save_merged_data(merged_data)

    # Merge with target organism transcriptome data
    merge_with_target_organism_transcriptome(merged_data, target_organism_transcriptome)