import argparse
import pandas as pd
import numpy as np
import re
import os
import sys
from Bio import SeqIO
import pybedtools
from scipy.stats import beta
from scipy.special import logsumexp
from RAISE.plot_target import plot_dpsi_with_alpha_beta
from RAISE.plot_target import plot_motif_param
from RAISE.plot_target import plot_clip_param


def parse_args():
    parser = argparse.ArgumentParser(
        description="EM algorithm for inferring RBP targets using motif, CLIP peaks, and PSI changes."
    )
    parser.add_argument('--rmats', type=str, required=True, help="Input rMATS SE.MATS.JC.txt file.")
    parser.add_argument('--clip_peaks', type=str, required=True, help="Input CLIP peaks BED file.")
    parser.add_argument('--ref_genome', type=str, required=True, help="Reference genome in FASTA format.")
    parser.add_argument('--rbp_motif', type=str, required=True, help="RBP motif file with two columns: RBP and motif.")
    parser.add_argument('--cell_line', type=str, required=True, help="Cell line name, used to label the output file.")
    parser.add_argument('--rbp', type=str, required=True, help="Target RBP name.")
    parser.add_argument('--output', type=str, required=True, help="Output directory.")
    parser.add_argument('--max_iter', type=int, default=1000, help="Maximum number of EM iterations.")
    parser.add_argument('--tol', type=float, default=1e-4, help="Convergence threshold for EM.")
    return parser.parse_args()


def extract_regions(row, genome, extend=200):
    """
    Extract upstream, exon, and downstream sequences for each exon-skipping event.
    """
    chrom = row["chr"]
    start = row["exonStart_0base"]
    end = row["exonEnd"]
    strand = row["strand"]
    seq_record = genome[chrom]

    up_start = max(start - extend, 0)
    up_seq = seq_record.seq[up_start:start]
    exon_seq = seq_record.seq[start:end]
    down_seq = seq_record.seq[end:end+extend]

    if strand == '-':
        from Bio.Seq import Seq
        up_seq, down_seq = down_seq, up_seq
        up_seq = up_seq.reverse_complement()
        exon_seq = exon_seq.reverse_complement()
        down_seq = down_seq.reverse_complement()

    return str(up_seq), str(exon_seq), str(down_seq)


def binary_motif(seq, motifs):
    """
    Return 1 if any motif is present in the sequence, else 0.
    """
    for motif in motifs:
        if re.search(motif, seq, flags=re.IGNORECASE):
            return 1
    return 0


def calculate_mean(value):
    """
    Compute the mean of comma-separated values in a string.
    """
    if pd.isna(value):
        return np.nan
    return np.mean([float(x) for x in value.split(',')])


def run_em(features_df, max_iter=1000, tol=1e-4):
    """
    Run EM algorithm to estimate parameters and compute posterior P(T=1 | data).
    """
    n = len(features_df)
    print(f"Total data points: {n}")

    # Initialize parameters
    p1 = np.array([0.6, 0.6, 0.6])
    p0 = np.array([0.4, 0.4, 0.4])
    q1 = np.array([0.6, 0.6, 0.6])
    q0 = np.array([0.4, 0.4, 0.4])
    alpha1, beta1 = 1, 3
    alpha0, beta0 = 1, 10
    pi1 = 0.05
    pi0 = 1 - pi1

    M = features_df[['M_upstream', 'M_exon', 'M_downstream']].values
    C = features_df[['C_upstream', 'C_exon', 'C_downstream']].values
    PSI = abs(features_df['PSI'].values)

    for iteration in range(max_iter):
        # E-step
        log_L_s1 = beta.logpdf(PSI + 1e-10, alpha1, beta1)
        log_L_s0 = beta.logpdf(PSI + 1e-10, alpha0, beta0)
        log_L_M1 = np.sum(M * np.log(p1 + 1e-10) + (1 - M) * np.log(1 - p1 + 1e-10), axis=1)
        log_L_M0 = np.sum(M * np.log(p0 + 1e-10) + (1 - M) * np.log(1 - p0 + 1e-10), axis=1)
        log_L_C1 = np.sum(C * np.log(q1 + 1e-10) + (1 - C) * np.log(1 - q1 + 1e-10), axis=1)
        log_L_C0 = np.sum(C * np.log(q0 + 1e-10) + (1 - C) * np.log(1 - q0 + 1e-10), axis=1)

        log_L1 = log_L_s1 + log_L_M1 + log_L_C1
        log_L0 = log_L_s0 + log_L_M0 + log_L_C0
        gamma = np.exp(np.log(pi1) + log_L1 - logsumexp([np.log(pi1) + log_L1, np.log(pi0) + log_L0], axis=0))

        # M-step
        pi1_new = np.mean(gamma)
        pi0_new = 1 - pi1_new
        p1_new = np.sum(gamma[:, None] * M, axis=0) / (np.sum(gamma) + 1e-10)
        p0_new = np.sum((1 - gamma)[:, None] * M, axis=0) / (np.sum(1 - gamma) + 1e-10)
        q1_new = np.sum(gamma[:, None] * C, axis=0) / (np.sum(gamma) + 1e-10)
        q0_new = np.sum((1 - gamma)[:, None] * C, axis=0) / (np.sum(1 - gamma) + 1e-10)

        # Beta distribution parameters
        if np.sum(gamma) > 0:
            mu1 = np.sum(gamma * PSI) / (np.sum(gamma) + 1e-10)
            sigma2_1 = np.sum(gamma * (PSI - mu1) ** 2) / (np.sum(gamma) + 1e-10)
            alpha1_new = max((mu1**2 * (1 - mu1)) / (sigma2_1 + 1e-10) - mu1, 1e-2)
            beta1_new = max(alpha1_new * (1 - mu1) / (mu1 + 1e-10), 1e-2)
        else:
            alpha1_new, beta1_new = alpha1, beta1

        if np.sum(1 - gamma) > 0:
            mu0 = np.sum((1 - gamma) * PSI) / (np.sum(1 - gamma) + 1e-10)
            sigma2_0 = np.sum((1 - gamma) * (PSI - mu0) ** 2) / (np.sum(1 - gamma) + 1e-10)
            alpha0_new = max((mu0**2 * (1 - mu0)) / (sigma2_0 + 1e-10) - mu0, 1e-2)
            beta0_new = max(alpha0_new * (1 - mu0) / (mu0 + 1e-10), 1e-2)
        else:
            alpha0_new, beta0_new = alpha0, beta0

        diff_norm = np.linalg.norm(np.array([
            pi1_new, *p1_new, *p0_new, *q1_new, *q0_new, alpha1_new, beta1_new, alpha0_new, beta0_new
        ]) - np.array([
            pi1, *p1, *p0, *q1, *q0, alpha1, beta1, alpha0, beta0
        ]), 1)

        print(f"Iteration {iteration+1}: diff_norm = {diff_norm:.6f}, pi1 = {pi1_new:.4f}")
        if diff_norm < tol:
            print(f"EM converged in iteration {iteration+1}")
            break

        pi1, p1, p0, q1, q0 = pi1_new, p1_new, p0_new, q1_new, q0_new
        alpha1, beta1, alpha0, beta0 = alpha1_new, beta1_new, alpha0_new, beta0_new

    features_df['P(T|S, M, C)'] = gamma
    params = {
        'pi1': pi1,
        'p1': p1.tolist(),
        'p0': p0.tolist(),
        'q1': q1.tolist(),
        'q0': q0.tolist(),
        'alpha1': alpha1,
        'beta1': beta1,
        'alpha0': alpha0,
        'beta0': beta0
    }
    return features_df, params


def main():
    args = parse_args()

    # Step 1: Load rMATS data
    df_rmats = pd.read_csv(args.rmats, sep="\t")
    df_rmats["event_id"] = df_rmats.apply(lambda row: f"{row['geneSymbol']}_{row['exonStart_0base']}_{row['exonEnd']}", axis=1)
    print("Loaded rMATS data.")

    # Step 2: Load genome
    ref_genome = SeqIO.to_dict(SeqIO.parse(args.ref_genome, "fasta"))
    print("Loaded reference genome.")

    # Step 3: Load CLIP peaks
    clip_peaks = pybedtools.BedTool(args.clip_peaks)
    print("Loaded CLIP BED file.")

    # Step 4: Load motif
    df_motif = pd.read_csv(args.rbp_motif, sep="\t", header=None, names=["RBP", "Motif"])
    rbp_motifs = df_motif[df_motif["RBP"] == args.rbp]["Motif"].tolist()
    if len(rbp_motifs) == 0:
        sys.exit("RBP not found in motif file.")
    print("Loaded RBP motif.")

    # Step 5: Generate motif and CLIP features
    M_minus, M_0, M_plus = [], [], []
    clip_intervals_minus, clip_intervals_exon, clip_intervals_plus = [], [], []

    for idx, row in df_rmats.iterrows():
        up_seq, exon_seq, down_seq = extract_regions(row, ref_genome, extend=200)
        M_minus.append(binary_motif(up_seq, rbp_motifs))
        M_0.append(binary_motif(exon_seq, rbp_motifs))
        M_plus.append(binary_motif(down_seq, rbp_motifs))

        chrom = row["chr"]
        start = row["exonStart_0base"]
        end = row["exonEnd"]
        strand = row["strand"]

        if strand == '+':
            up_iv = pybedtools.Interval(chrom, max(start - 200, 0), start, name=str(idx))
            exon_iv = pybedtools.Interval(chrom, start, end, name=str(idx))
            down_iv = pybedtools.Interval(chrom, end, end + 200, name=str(idx))
        else:
            down_iv = pybedtools.Interval(chrom, max(start - 200, 0), start, name=str(idx))
            exon_iv = pybedtools.Interval(chrom, start, end, name=str(idx))
            up_iv = pybedtools.Interval(chrom, end, end + 200, name=str(idx))

        clip_intervals_minus.append(up_iv)
        clip_intervals_exon.append(exon_iv)
        clip_intervals_plus.append(down_iv)

    print("Generated motif features.")

    # Step 6: Intersect with CLIP peaks
    clip_minus = pybedtools.BedTool(clip_intervals_minus).intersect(clip_peaks, u = True)
    clip_minus_names = set(iv.name for iv in clip_minus)
    clip_exon = pybedtools.BedTool(clip_intervals_exon).intersect(clip_peaks, u = True)
    clip_exon_names = set(iv.name for iv in clip_exon)
    clip_plus = pybedtools.BedTool(clip_intervals_plus).intersect(clip_peaks, u = True)
    clip_plus_names = set(iv.name for iv in clip_plus)


    C_minus = [1 if iv.name in clip_minus_names else 0 for iv in clip_intervals_minus]
    C_0 = [1 if iv.name in clip_exon_names else 0 for iv in clip_intervals_exon]
    C_plus = [1 if iv.name in clip_plus_names else 0 for iv in clip_intervals_plus]
    print("Generated CLIP features.")

    # Step 7: Assign values
    df_rmats["M_minus"], df_rmats["M_0"], df_rmats["M_plus"] = M_minus, M_0, M_plus
    df_rmats["C_minus"], df_rmats["C_0"], df_rmats["C_plus"] = C_minus, C_0, C_plus

    for col in ["IJC_SAMPLE_1", "SJC_SAMPLE_1", "IJC_SAMPLE_2", "SJC_SAMPLE_2"]:
        df_rmats[col + "_mean"] = df_rmats[col].apply(calculate_mean)

    df_rmats["S"] = df_rmats.apply(lambda row: row["IncLevelDifference"] if row["PValue"] < 0.05 else np.nan, axis=1)
    df_rmats = df_rmats.dropna(subset=['S'])
    df_rmats["S"] = df_rmats.apply(lambda row: row["S"] if (row["IJC_SAMPLE_1_mean"] + row["SJC_SAMPLE_1_mean"] >= 20 or row["IJC_SAMPLE_2_mean"] + row["SJC_SAMPLE_2_mean"] >= 20) else np.nan, axis=1)
    df_rmats = df_rmats.dropna(subset=['S'])
    print("Calculated PSI changes.")

    # Step 8: Prepare for EM
    features_df = df_rmats.rename(columns={
        "M_minus": "M_upstream", "M_0": "M_exon", "M_plus": "M_downstream",
        "C_minus": "C_upstream", "C_0": "C_exon", "C_plus": "C_downstream",
        "S": "PSI"
    })

    features_df, params = run_em(features_df, max_iter=args.max_iter, tol=args.tol)

    # Step 9: Save results
    basename = f"{args.cell_line}_{args.rbp}"
    output_dir = os.path.join(args.output, basename)
    os.makedirs(output_dir, exist_ok=True)
    param_file = os.path.join(output_dir, basename + '_param.txt')
    target_file = os.path.join(output_dir, basename + '_target.txt')
    dpsi_plot = os.path.join(output_dir, basename + '_dPSI.png')
    motif_plot = os.path.join(output_dir, basename + '_Motif.png')
    clip_plot = os.path.join(output_dir, basename + '_CLIP.png')

    try:
        with open(param_file, "w") as fout:
            fout.write("EM algorithm parameters:\n")
            for key, value in params.items():
                fout.write(f"{key}: {value}\n")
        features_df.sort_values(by='P(T|S, M, C)', ascending=False).to_csv(target_file, sep="\t", index=False)
        print(f"Results saved to {output_dir}")
    except Exception as e:
        sys.exit(f"Error saving output: {e}")

    plot_dpsi_with_alpha_beta(df=features_df,
                              alpha1=params['alpha1'], 
                              beta1=params['beta1'], 
                              alpha0=params['alpha0'], 
                              beta0=params['beta0'], 
                              threshold=0.6, 
                              output_file=dpsi_plot)
    
    plot_motif_param(df=features_df,
                     p1=params['p1'],
                     p0=params['p0'],
                     threshold=0.6,
                     output_file=motif_plot)
    
    plot_clip_param(df=features_df,
                     q1=params['q1'],
                     q0=params['q0'],
                     threshold=0.6,
                     output_file=clip_plot)
    


if __name__ == "__main__":
    main()
