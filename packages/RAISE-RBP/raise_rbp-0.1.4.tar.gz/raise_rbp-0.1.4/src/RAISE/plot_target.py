import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import beta
from matplotlib.colors import LinearSegmentedColormap

def plot_dpsi_with_alpha_beta(df, alpha1, beta1, alpha0, beta0, threshold=0.6, output_file="dpsi_plot.png"):
    """
    Plot the distribution of |IncLevelDifference| for target and non-target events,
    and overlay fitted Beta distributions.
    """
    df_target = df[df["P(T|S, M, C)"] >= threshold]
    df_nontarget = df[df["P(T|S, M, C)"] < threshold]

    plt.figure(figsize=(8, 6))

    # Plot for target events
    plt.subplot(2, 1, 1)
    sns.histplot(abs(df_target["IncLevelDifference"]), bins=50, stat="density", color="grey", alpha=0.3)
    sns.kdeplot(abs(df_target["IncLevelDifference"]), label="delta PSI", fill=True, color="blue", alpha=0.5)
    x_beta = np.linspace(0, 1, 100)
    y_beta = beta.pdf(x_beta, alpha1, beta1)
    plt.plot(x_beta, y_beta, 'r-', label=f'Beta (α={alpha1}, β={beta1})', linewidth=2)
    plt.title("Target Events")

    # Plot for non-target events
    plt.subplot(2, 1, 2)
    sns.histplot(abs(df_nontarget["IncLevelDifference"]), bins=50, stat="density", color="grey", alpha=0.3)
    sns.kdeplot(abs(df_nontarget["IncLevelDifference"]), label="delta PSI", fill=True, color="blue", alpha=0.5)
    x_beta = np.linspace(0, 1, 100)
    y_beta = beta.pdf(x_beta, alpha0, beta0)
    plt.plot(x_beta, y_beta, 'r-', label=f'Beta (α={alpha0}, β={beta0})', linewidth=2)
    plt.title("Non-target Events")

    # Common axis labels and legend
    for ax in plt.gcf().axes:
        ax.set_xlabel("IncLevelDifference")
        ax.set_ylabel("Density")
        ax.legend()

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Plot saved to {output_file}")


def plot_motif_param(df, p1, p0, threshold=0.6, output_file="motif_plot.png"):
    """
    Plot motif occurrence in target/non-target groups and compare motif parameters.
    """

    # Count motif presence in target and non-target groups
    df_target_up = len(df[(df["P(T|S, M, C)"] >= threshold) & (df["M_upstream"] == 1)])
    df_target_ex = len(df[(df["P(T|S, M, C)"] >= threshold) & (df["M_exon"] == 1)])
    df_target_dn = len(df[(df["P(T|S, M, C)"] >= threshold) & (df["M_downstream"] == 1)])
    df_nontarget_up = len(df[(df["P(T|S, M, C)"] < threshold) & (df["M_upstream"] == 1)])
    df_nontarget_ex = len(df[(df["P(T|S, M, C)"] < threshold) & (df["M_exon"] == 1)])
    df_nontarget_dn = len(df[(df["P(T|S, M, C)"] < threshold) & (df["M_downstream"] == 1)])

    # Create plot
    plt.figure(figsize=(12, 5))

    # Heatmap of motif parameters
    plt.subplot(1, 2, 1)
    param_matrix = np.vstack([p1, p0])
    cmap = LinearSegmentedColormap.from_list("excel_style", ["#63BE7B", "#FFEB84", "#F8696B"])
    ax = sns.heatmap(param_matrix, vmin=0, vmax=1, annot_kws={"color": "black", "size": 10}, cmap=cmap, xticklabels=["Upstream", "Exon", "Downstream"], yticklabels=["Target", "Non-target"])
    for i in range(param_matrix.shape[0]):
        for j in range(param_matrix.shape[1]):
            text_color = "white" if param_matrix[i, j] > 0.4 else "black"
            ax.text(j + 0.5, i + 0.5, f"{param_matrix[i, j]:.5f}",
                    ha='center', va='center', color=text_color, fontsize=10)
            
    # Bar plot of motif occurance
    plt.subplot(1, 2, 2)
    labels = ["Upstream", "Exon", "Downstream"]
    target_counts = [df_target_up, df_target_ex, df_target_dn]
    nontarget_counts = [df_nontarget_up, df_nontarget_ex, df_nontarget_dn]

    x = np.arange(len(labels))
    width = 0.35

    plt.bar(x - width/2, target_counts, width, label='Target', color='steelblue')
    plt.bar(x + width/2, nontarget_counts, width, label='Non-target', color='salmon')

    plt.xticks(x, labels)
    plt.ylabel("Event Count")
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Motif plot saved to {output_file}")

def plot_clip_param(df, q1, q0, threshold=0.6, output_file="clip_plot.png"):
    """
    Plot CLIP peak occurrence in target/non-target groups and compare CLIP parameters.
    """

    # Count CLIP peak presence in target and non-target groups
    df_target_up = len(df[(df["P(T|S, M, C)"] >= threshold) & (df["C_upstream"] == 1)])
    df_target_ex = len(df[(df["P(T|S, M, C)"] >= threshold) & (df["C_exon"] == 1)])
    df_target_dn = len(df[(df["P(T|S, M, C)"] >= threshold) & (df["C_downstream"] == 1)])
    df_nontarget_up = len(df[(df["P(T|S, M, C)"] < threshold) & (df["C_upstream"] == 1)])
    df_nontarget_ex = len(df[(df["P(T|S, M, C)"] < threshold) & (df["C_exon"] == 1)])
    df_nontarget_dn = len(df[(df["P(T|S, M, C)"] < threshold) & (df["C_downstream"] == 1)])

    # Create plot
    plt.figure(figsize=(12, 5))

    # Heatmap of CLIP parameters
    plt.subplot(1, 2, 1)
    param_matrix = np.vstack([q1, q0])
    param_matrix = np.array(param_matrix, dtype=np.float64)
    cmap = LinearSegmentedColormap.from_list("excel_style", ["#63BE7B", "#FFEB84", "#F8696B"])
    ax = sns.heatmap(param_matrix, vmin=0, vmax=1, annot_kws={"color": "black", "size": 10}, cmap=cmap, xticklabels=["Upstream", "Exon", "Downstream"], yticklabels=["Target", "Non-target"])
    for i in range(param_matrix.shape[0]):
        for j in range(param_matrix.shape[1]):
            text_color = "white" if param_matrix[i, j] > 0.4 else "black"
            ax.text(j + 0.5, i + 0.5, f"{param_matrix[i, j]:.5f}",
                    ha='center', va='center', color=text_color, fontsize=10)

    # Bar plot of CLIP peak occurance
    plt.subplot(1, 2, 2)
    labels = ["Upstream", "Exon", "Downstream"]
    target_counts = [df_target_up, df_target_ex, df_target_dn]
    nontarget_counts = [df_nontarget_up, df_nontarget_ex, df_nontarget_dn]

    x = np.arange(len(labels))
    width = 0.35

    plt.bar(x - width/2, target_counts, width, label='Target', color='steelblue')
    plt.bar(x + width/2, nontarget_counts, width, label='Non-target', color='salmon')

    plt.xticks(x, labels)
    plt.ylabel("Event Count")
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"CLIP plot saved to {output_file}")
