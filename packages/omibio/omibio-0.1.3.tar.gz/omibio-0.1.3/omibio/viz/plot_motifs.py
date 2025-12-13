import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from omibio.bio import SeqInterval, AnalysisResult


def plot_motifs(
    motifs: list[SeqInterval] | AnalysisResult,
    seq_length: int | None = None,
    ax: Axes | None = None,
    show: bool = False
) -> Axes:

    if ax is None:
        ax = plt.subplots(figsize=(9, 3))[1]
    if seq_length is None:
        if isinstance(motifs, AnalysisResult):
            seq_length = motifs.metadata["seq_length"]
        else:
            raise TypeError(
                "plot_motifs() argument: 'seq_length' must be provided if"
                "'motifs' is a list"
            )

    strand_y = {"+": 2, "-": 1}
    color_mp = {"+": "#4D84DC", "-": "#E14040"}
    ax.axhline(y=2, color="#4D84DC", linestyle="-", zorder=0)
    ax.axhline(y=1, color="#E14040", linestyle="-", zorder=0)
    handle_plus = ax.scatter(
        [], [], color=color_mp["+"], marker=">", label="Positive strand (+)"
    )
    handle_minus = ax.scatter(
        [], [], color=color_mp["-"], marker="<", label="Negative strand (-)"
    )

    for motif in motifs:
        color = color_mp[motif.strand]
        marker = ">" if motif.strand == "+" else "<"

        ax.scatter(
            x=motif.start, y=strand_y[motif.strand], s=70,
            facecolors=color, marker=marker, zorder=3
        )

    ax.set_ylim(0, 3)
    ax.set_xlim(-1, seq_length+1)
    ax.set_yticks([2, 1])
    ax.set_yticklabels(["+", "-"])
    ax.set_xlabel("Sequence Position")
    ax.set_ylabel("Strand")
    ax.set_title("Motif Distribution")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(handles=[handle_plus, handle_minus])

    if show:
        plt.show()
    return ax


def main():
    from omibio.analysis import find_motifs
    from omibio.io import read_fasta

    seq = read_fasta(
        r"./examples/data/example_single_short_seq.fasta"
    )["example"]
    res = find_motifs(seq, "ACT", include_reverse=True)
    plot_motifs(res, show=True)


if __name__ == "__main__":
    main()
