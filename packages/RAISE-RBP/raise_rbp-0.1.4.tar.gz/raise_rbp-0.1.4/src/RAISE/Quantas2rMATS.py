import pandas as pd
import argparse
import numpy as np

def read_multiple_files(file_list):
    return [pd.read_csv(f, sep='\t', header=0) for f in file_list]

def extract_column_values(df_list, gene_id_col, target_col_indices, compute_avg=False):
    result_dict = {}

    for df in df_list:
        for _, row in df.iterrows():
            gene_id = row[gene_id_col]
            if compute_avg:
                value = (row[target_col_indices[0]] + row[target_col_indices[1]]) / 2
            else:
                value = row[target_col_indices[0]]

            if gene_id in result_dict:
                result_dict[gene_id].append(str(int(value)))
            else:
                result_dict[gene_id] = [str(int(value))]

    return {gene_id: ",".join(values) for gene_id, values in result_dict.items()}

def main(input_ds, input_exon, input_up, input_down, group1_files, group2_files, output_file, r):
    # Load input files
    DS = pd.read_csv(input_ds, sep='\t', header=0)
    exon = pd.read_csv(input_exon, sep='\t', header=None)
    up = pd.read_csv(input_up, sep='\t', header=None)
    down = pd.read_csv(input_down, sep='\t', header=None)

    # Load multiple group files
    group1_list = read_multiple_files(group1_files.split(','))
    group2_list = read_multiple_files(group2_files.split(','))

    # Filter DS to retain rows with GeneID present in exon file
    valid_gene_ids = exon.iloc[:, 3].unique()
    DS = DS[DS.iloc[:, 4].isin(valid_gene_ids)]

    # Initialize output DataFrame
    output = pd.DataFrame()
    output['ID'] = range(1, len(DS) + 1)
    output['GeneID'] = DS.iloc[:, 4]
    output['geneSymbol'] = DS.iloc[:, 0]
    output['chr'] = DS.iloc[:, 1]
    output['strand'] = DS.iloc[:, 6]

    # Rename exon columns and merge coordinates
    exon.columns = ['col1', 'exonStart_0base', 'exonEnd', 'GeneID', 'score', 'strand']
    output = output.merge(exon[['GeneID', 'exonStart_0base', 'exonEnd']], on='GeneID', how='left')

    # Calculate upstream and downstream exon coordinates
    def calculate_up_down(row):
        gene_id = row['name']
        strand = row['strand']
        try:
            if strand == '+':
                upstreamES = int(row[DS.columns[2]])  
                upstreamEE = int(up.loc[up.iloc[:, 3] == gene_id, 1].values[0])
                downstreamES = int(down.loc[down.iloc[:, 3] == gene_id, 2].values[0])
                downstreamEE = int(row[DS.columns[3]])  
            else:
                upstreamES = int(row[DS.columns[2]])  
                upstreamEE = int(down.loc[down.iloc[:, 3] == gene_id, 1].values[0])
                downstreamES = int(up.loc[up.iloc[:, 3] == gene_id, 2].values[0])
                downstreamEE = int(row[DS.columns[3]])  
        except IndexError:
            return pd.Series([None, None, None, None])

        return pd.Series([upstreamES, upstreamEE, downstreamES, downstreamEE])

    output[['upstreamES', 'upstreamEE', 'downstreamES', 'downstreamEE']] = DS.apply(calculate_up_down, axis=1)

    # Extract IJC/SJC values from group files
    ijc_sample_1 = extract_column_values(group1_list, gene_id_col=3, target_col_indices=[11, 12], compute_avg=True)
    sjc_sample_1 = extract_column_values(group1_list, gene_id_col=3, target_col_indices=[13], compute_avg=False)
    ijc_sample_2 = extract_column_values(group2_list, gene_id_col=3, target_col_indices=[11, 12], compute_avg=True)
    sjc_sample_2 = extract_column_values(group2_list, gene_id_col=3, target_col_indices=[13], compute_avg=False)

    output['IJC_SAMPLE_1'] = output['GeneID'].map(ijc_sample_1).fillna('0')
    output['SJC_SAMPLE_1'] = output['GeneID'].map(sjc_sample_1).fillna('0')
    output['IJC_SAMPLE_2'] = output['GeneID'].map(ijc_sample_2).fillna('0')
    output['SJC_SAMPLE_2'] = output['GeneID'].map(sjc_sample_2).fillna('0')

    # Calculate IncFormLen and SkipFormLen
    a = 1
    e = abs(output['exonStart_0base'] - output['exonEnd'])

    output['IncFormLen'] = r - 2*a + 1 + np.minimum(e, r - 2*a + 1)
    output['SkipFormLen'] = r - 2*a + 1

    output['PValue'] = DS.iloc[:, 13]
    output['FDR'] = DS.iloc[:, 14]

    # Calculate IncLevel1 and IncLevel2
    def compute_inclevel(ijc, sjc):
        ijc_list = list(map(int, ijc.split(',')))
        sjc_list = list(map(int, sjc.split(',')))
        inclevel = [round(i / (i + s) if (i + s) > 0 else 0, 3) for i, s in zip(ijc_list, sjc_list)]
        return ",".join(map(str, inclevel))

    output['IncLevel1'] = output.apply(lambda row: compute_inclevel(row['IJC_SAMPLE_1'], row['SJC_SAMPLE_1']), axis=1)
    output['IncLevel2'] = output.apply(lambda row: compute_inclevel(row['IJC_SAMPLE_2'], row['SJC_SAMPLE_2']), axis=1)

    # Insert ID2 column
    output.insert(output.columns.get_loc('downstreamEE') + 1, 'ID2', output['ID'])

    # Calculate IncLevelDifference
    def compute_avg_inclevel(inclevel_str):
        levels = list(map(float, inclevel_str.split(',')))
        return sum(levels) / len(levels) if levels else 0

    output['IncLevelDifference'] = output.apply(
        lambda row: round(compute_avg_inclevel(row['IncLevel1']) - compute_avg_inclevel(row['IncLevel2']), 3), axis=1
    )

    # Filter out rows where all four junction count columns are zeros
    def all_values_are_zero(value):
        return all(v == "0" for v in value.split(","))

    mask = ~(
        output['IJC_SAMPLE_1'].apply(all_values_are_zero) &
        output['SJC_SAMPLE_1'].apply(all_values_are_zero) &
        output['IJC_SAMPLE_2'].apply(all_values_are_zero) &
        output['SJC_SAMPLE_2'].apply(all_values_are_zero)
    )
    output = output[mask]

    # Write final output
    column_names = [
        "ID", "GeneID", "geneSymbol", "chr", "strand", "exonStart_0base", "exonEnd", 
        "upstreamES", "upstreamEE", "downstreamES", "downstreamEE", "ID", 
        "IJC_SAMPLE_1", "SJC_SAMPLE_1", "IJC_SAMPLE_2", "SJC_SAMPLE_2", "IncFormLen", 
        "SkipFormLen", "PValue", "FDR", "IncLevel1", "IncLevel2", "IncLevelDifference"
    ]

    with open(output_file, 'w') as f:
        f.write('\t'.join(column_names))
        f.write('\n')
        output.to_csv(f, sep='\t', header=False, index=False, quotechar='"')
    print(f"Output file generated: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Quantas output format into rMATS-compatible format.")
    parser.add_argument("--ds", required=True, help="The output file from test_splicing_diff.pl (Quantas differential splicing results).")
    parser.add_argument("--exon", required=True, help="Exon coordinate file (e.g., exon.bed from data/).")
    parser.add_argument("--up", required=True, help="Upstream exon coordinate file (e.g., upstream.bed from data/).")
    parser.add_argument("--down", required=True, help="Downstream exon coordinate file (e.g., downstream.bed from data/).")
    parser.add_argument("--group1", required=True, help="Comma-separated Quantas output files (from summarize_splicing_wrapper.pl) for Group 1 samples.")
    parser.add_argument("--group2", required=True, help="Comma-separated Quantas output files (from summarize_splicing_wrapper.pl) for Group 2 samples.")
    parser.add_argument("--output", required=True, help="Output file path in rMATS-compatible format.")
    parser.add_argument("--r", required=True, type=int, help="Read length used in the sequencing experiment.")


    args = parser.parse_args()
    main(args.ds, args.exon, args.up, args.down, args.group1, args.group2, args.output, args.r)
