import sys
import pandas as pd
import re
from Bio import Blast, Entrez, SeqIO

Entrez.email = "sudipta@pusan.ac.kr"
def get_sequence_type(seq: str) -> str:
    if not seq:
        raise ValueError("Empty sequence provided")
    seq = seq.upper().strip()
    dna_chars = set('ATGCN')
    rna_chars = set('AUGCN')
    protein_chars = set('ACDEFGHIKLMNPQRSTVWY*')

    seq_chars = set(seq)
    if seq_chars.issubset(dna_chars):
        if 'T' in seq_chars:
            return 'DNA'
        elif 'U' in seq_chars:
            return 'RNA'
        else:
            return 'DNA'

    elif seq_chars.issubset(rna_chars):
        return 'RNA'

    elif seq_chars.issubset(protein_chars):
        return 'Protein'

    else:
        invalid_chars = seq_chars - (dna_chars | rna_chars | protein_chars)
        raise ValueError(f"Invalid sequence. Contains unexpected characters: {invalid_chars}")
def blast(sequence):
    print('Starting Blast')
    response = Blast.qblast(program='tblastn',
                            database='core_nt',
                            sequence=sequence,
                            format_type='XML')
    blast_record = Blast.read(response)
    ##getting the alignment of the top sequence
    alignment = blast_record[0][0].target.features[0].qualifiers.get('coded_by').split('|')
    ncbi_gi, ncbi_id, positions = alignment[1], alignment[3], alignment[4]
    start_pos, end_pos = positions.split(':')[1].split('..')
    if int(start_pos) > int(end_pos):
        start_pos, end_pos = end_pos, start_pos
    return ncbi_gi, ncbi_id, start_pos, end_pos

def retrieve_seq(ncbi_id, start_pos, end_pos):
    print(f'Retrieving Sequence with NCBI ID: {ncbi_id}')
    handle = Entrez.efetch(db='nucleotide', id=ncbi_id, rettype='fasta', retmode='text')
    record = SeqIO.read(handle, 'fasta')
    seq_of_interest = record.seq[int(start_pos)-1:int(end_pos)-1]
    return seq_of_interest
def validator(mirna_ids: str, mrna: str) -> pd.DataFrame:
    df = pd.read_excel("data/data.xlsx", engine="openpyxl")
    mirna_id_list = mirna_ids.split(',')
    
    input_seq_type = get_sequence_type(mrna)
    if input_seq_type == "DNA":
        dna_seq = mrna.lower().strip()
    elif input_seq_type == "RNA":
        dna_seq = mrna.lower().replace('u', 't').strip()
    elif input_seq_type == "Protein":
        ncbi_gi, ncbi_id, start_pos, end_pos = blast(mrna)
        print(f'NCBI GI: {ncbi_gi}')
        dna_seq = str(retrieve_seq(ncbi_id, start_pos, end_pos)).lower().strip()
    else:
        raise ValueError("Invalid mRNA sequence type.")

    matching_rows = []
    for mirna_id in mirna_id_list:
        mirna_id = mirna_id + " "
        if mirna_id in df['Human miRNA ID'].values:
            # Get rows where 'Human miRNA ID' matches mirna_id
            rows = df[df['Human miRNA ID'] == mirna_id]
            matching_rows.append(rows)

    if matching_rows:
        result_df = pd.concat(matching_rows)
        
        for index, row in result_df.iterrows():
            seeds = row[-3:].values
            result_df.at[index, 'interaction'] = any(re.search(seed, dna_seq.lower()) for seed in seeds if pd.notna(seed))
        
        print(result_df[['Human miRNA ID', 'interaction']])

        wanna_save = input("Do you want to save this result? (y/n): ").strip().lower()
        if wanna_save == 'y':
            result_df.to_csv("validator_output.csv", index=False)
            print("Result saved to 'validator_output.csv'.")
        elif wanna_save == 'n':
            print("You chose not to save the result.")
        else:
            print("Invalid input. Result not saved.")

    else:
        print("No matching miRNA IDs found.")

def cli():
    """CLI entry point for validator"""
    if len(sys.argv) != 3:
        print("Usage: validator <miRNA_sequence> <mRNA_sequence>")
        sys.exit(1)
    validator(sys.argv[1], sys.argv[2])
