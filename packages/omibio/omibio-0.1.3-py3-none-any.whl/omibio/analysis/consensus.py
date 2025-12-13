from omibio.io.read_fasta import read_fasta
from omibio.sequence.sequence import Sequence
from collections import defaultdict

IUPAC_CODES = {
    frozenset({'A', 'G'}): 'R', frozenset({'C', 'T'}): 'Y',
    frozenset({'G', 'C'}): 'S', frozenset({'A', 'T'}): 'W',
    frozenset({'G', 'T'}): 'K', frozenset({'A', 'C'}): 'M',
    frozenset({"C", "G", "T"}): "B", frozenset({"A", "G", "T"}): "D",
    frozenset({"A", "C", "T"}): "H", frozenset({"A", "C", "G"}): "V"
}


def find_consensus(
    seq_list: list[str | Sequence],
    as_str: bool = False,
    gap_chars: str = "-?.",
    as_rna: bool = False
) -> str | Sequence:
    """Finds the consensus sequence from a list of sequences.

    Args:
        seq_list (list[str  |  Sequence]):
            list of sequences to find consensus from.
        as_str (bool, optional):
            whether to return the consensus as a string.
            Defaults to False.
        gap_chars (str, optional):
            characters to consider as gaps. Defaults to "-?.".
        as_rna (bool, optional):
            whether to return the consensus as RNA sequence.
            Defaults to False.

    Raises:
        TypeError: If seq_list is not a list.
        ValueError: If sequences are not of the same length.

    Returns:
        str | Sequence: The consensus sequence as a string or Sequence object.
    """

    if not seq_list:
        return ""
    if not isinstance(seq_list, list):
        raise TypeError(
            "find_consensus() argument 'seq_list' must be list, got "
            + type(seq_list).__name__
        )
    seq_list = [str(s).upper() for s in seq_list]

    lengths = set(map(len, seq_list))
    if len(lengths) != 1:
        raise ValueError("All sequences must be of the same length")

    consensus_list = []

    for i in range(lengths.pop()):
        base_scores: defaultdict[str, int] = defaultdict(int)
        for seq in seq_list:
            base = seq[i].replace("U", "T")
            if base in gap_chars:
                continue
            base_scores[base] += 1

        if not base_scores:
            consensus_list.append("N")
            continue

        max_score = max(base_scores.values())
        top_base = [
            b for b, score in base_scores.items() if score == max_score
        ]
        if len(top_base) == 1:
            consensus_list.append(top_base[0])
        else:
            consensus_list.append(IUPAC_CODES.get(frozenset(top_base), "N"))

    consensus_seq = "".join(consensus_list)
    consensus = (
        Sequence(consensus_seq, strict=False) if not as_rna
        else Sequence(consensus_seq.replace("T", "U"), strict=False)
    )

    return consensus_seq if as_str else consensus


def main():
    input_file = r"./examples/data/example_short_seqs.fasta"
    sequences = read_fasta(input_file).seqs()
    consensus = find_consensus(sequences, as_rna=False)
    print(consensus)


if __name__ == "__main__":
    main()
