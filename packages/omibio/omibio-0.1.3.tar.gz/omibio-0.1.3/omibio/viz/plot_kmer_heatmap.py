import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
import matplotlib.pyplot as plt


def plot_kmer(
    kmer_counts: dict[str, int],
    ax=None,
    cmap='Blues',
    annot=True,
    fmt=".2f",
    show: bool = False
) -> Axes:
    if ax is None:
        ax = plt.subplots(figsize=(5, 5))[1]

    df = pd.DataFrame.from_dict(kmer_counts, orient='index', columns=['count'])
    df['freq'] = df['count'] / df['count'].sum()
    plot_data = df[['freq']]

    plot_data = plot_data.sort_values(by=plot_data.columns[0], ascending=False)

    sns.heatmap(plot_data, ax=ax, cmap=cmap, annot=annot, fmt=fmt, cbar=True)
    ax.set_ylabel('k-mer')
    ax.set_xlabel('Sample')
    ax.set_title('k-mer Frequency Heatmap')
    ax.yaxis.set_tick_params(rotation=0)

    if show:
        plt.show()
    return ax


def main():
    from omibio.analysis.kmer import kmer
    from omibio.io import read_fasta
    seq = read_fasta(
        "./examples/data/example_single_short_seq.fasta"
    )["example"]
    kmer_counts = kmer(seq, k=2)
    plot_kmer(kmer_counts)
    plt.show()


if __name__ == "__main__":
    main()
