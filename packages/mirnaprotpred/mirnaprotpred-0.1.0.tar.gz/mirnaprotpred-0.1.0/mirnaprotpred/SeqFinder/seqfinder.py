import sys
import pandas as pd
from Bio import Blast, Entrez, SeqIO
import RNA
import pyfiglet
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


def preprocess_bad_character_table(pattern):
    table = {}
    for i in range(len(pattern)):
        table[pattern[i]] = len(pattern) - i - 1
    return table
def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)
    if m > n:
        return []

    table = preprocess_bad_character_table(pattern)
    occurrences = []

    i = m - 1
    while i < n:
        j = m - 1
        while j >= 0 and text[i] == pattern[j]:
            i -= 1
            j -= 1

        if j == -1:
            occurrences.append(i + 1)

        bad_char_skip = table.get(text[i], m)
        i += max(m - j, bad_char_skip)

    return occurrences

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


def SeqFinder(seq: str) -> None:
    df = pd.read_excel(io="data/data.xlsx", engine="openpyxl")
    seq_type = get_sequence_type(seq)
    if seq_type == 'DNA':
        print("Processing DNA sequence...")
        dna_sequence = seq.lower().strip()
    elif seq_type == 'RNA':
        print("Processing RNA sequence...")
        dna_sequence = seq.lower().replace('u', 't').strip()
    elif seq_type == 'Protein':
        print("Processing Protein sequence...")
        ncbi_gi, ncbi_id, start_pos, end_pos = blast(seq)
        print(f'NCBI GI: {ncbi_gi}')
        dna_sequence = str(retrieve_seq(ncbi_id, start_pos, end_pos)).lower().strip()
    else:
        raise ValueError("Please Check Your Sequence...")
    
    target_sequences = [seq for col in ["seed1", "seed2", "seed3"] if col in df.columns for seq in df[col].dropna().tolist()]
    target_sequence_matches = [(seq, boyer_moore_search(dna_sequence, seq)) for seq in target_sequences if boyer_moore_search(dna_sequence, seq)]
    print(f"Found {len(target_sequence_matches)} matching target sequences.")
    matching_rows_df = pd.DataFrame(columns=df.columns.tolist() + ["Seed", "Position"])
    added_rows = set()
    for target_sequence, occurrences in target_sequence_matches:
        matching_rows = df[df.isin([target_sequence]).any(axis=1)]
        matching_rows = matching_rows[~matching_rows.index.isin(added_rows)]
                
        if not matching_rows.empty:
            for occurrence in occurrences:
                occurrence_row = matching_rows.copy()
                occurrence_row["Seed"] = target_sequence
                occurrence_row["Position"] = occurrence + 1
                matching_rows_df = pd.concat([matching_rows_df, occurrence_row])
                added_rows.update(matching_rows.index)
    display_rows = matching_rows_df.sort_values(by=["Position"], ascending=True).reset_index(drop=True).drop_duplicates()
    display_rows = display_rows[["Description", "Human miRNA ID", "Accession", "Sequence", "Seed", "Position"]]

    # sort with ViennaRNA MFE
    for index, row in display_rows.iterrows():
        mirna_seq = row['Sequence']
        if row['Position'] > 2:
            mrna_seq = str(dna_sequence[row['Position'] - 2: row['Position'] - 1 + len(mirna_seq)]).lower().replace('T', 'U')
        else:
            mrna_seq = str(dna_sequence[0: len(mirna_seq)]).lower().replace('T', 'U')

        # Create duplex
        duplex = RNA.duplexfold(mirna_seq, mrna_seq)
        energy = duplex.energy
        display_rows.at[index, 'CTS'] = mrna_seq.upper().strip()
        display_rows.at[index, 'MFE'] = energy
        if energy <= -15:
            display_rows.at[index, 'Prob'] = 'High'
        elif -15 < energy <= -10:
            display_rows.at[index, 'Prob'] = 'Medium'
        else:
            display_rows.at[index, 'Prob'] = 'Low'

    display_rows = display_rows.sort_values(by=['MFE'], ascending=True).reset_index(drop=True)
    print(display_rows)
    wanna_save = input("Do you want to save the result? (y/n): ").strip().lower()
    if wanna_save == 'y':
        display_rows.to_csv("SeqFinder_results.csv", index=False)
        print("Results saved to SeqFinder_results.csv")
    elif wanna_save == 'n':
        print("You chose not to save the results.")
    else:
        print("Invalid input. Results not saved.")

def cli():
    tool_name = pyfiglet.figlet_format("SeqFinder")
    print(tool_name)
    if len(sys.argv) != 2:
        print("Usage: SeqFinder <sequence>")
        sys.exit(1)
    SeqFinder(sys.argv[1])
