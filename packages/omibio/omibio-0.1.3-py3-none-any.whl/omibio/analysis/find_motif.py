from omibio.sequence.sequence import Sequence
from omibio.bio import SeqInterval, AnalysisResult
from omibio.viz.plot_motifs import plot_motifs
from typing import Pattern
import re


def find_motifs(
    seq: Sequence | str,
    pattern: str | Pattern,
    include_reverse: bool = False,
    seq_id: str | None = None,
    ignore_case: bool = True
) -> AnalysisResult:
    """Finds all occurrences of a motif in a given sequence.

    Args:
        seq (Sequence | str):
            the sequence to search within.
        pattern (str | Pattern):
            the motif pattern to search for. Can be a string or compiled regex.
        seq_id (str | None, optional):
            an optional identifier for the sequence. Defaults to None.
        ignore_case (bool, optional):
            whether to ignore case when searching. Defaults to True.

    Raises:
        TypeError: If seq is not a string or Sequence.
        TypeError: If pattern is not a string or compiled Pattern.
        ValueError: If pattern is an empty string.

    Returns:
        list[SeqInterval]:
            A list of SeqInterval objects representing motif occurrences.
    """

    if not isinstance(seq, (str, Sequence)):
        raise TypeError(
            "find_motifs() argument 'seq' must be str or Sequence, "
            f"got {type(seq).__name__}"
        )

    if isinstance(pattern, str):
        if not pattern:
            raise ValueError(
                "find_motifs() argument 'pattern' cannot be an empty string"
            )
        compiled_pat = (
            re.compile(re.escape(pattern), flags=re.IGNORECASE) if ignore_case
            else re.compile(re.escape(pattern))
        )
    elif isinstance(pattern, Pattern):
        flags = pattern.flags
        if ignore_case:
            flags |= re.IGNORECASE
        else:
            flags &= ~re.IGNORECASE  # Remove IGNORECASE if present
        compiled_pat = re.compile(pattern.pattern, flags=flags)
    else:
        raise TypeError(
            "find_motifs() argument 'pattern' must be str or compiled Pattern,"
            f" got {type(pattern).__name__}"
        )

    results = []
    n = len(seq)

    def find_motifs_in_strand(seq_str: str, strand):
        for match in compiled_pat.finditer(seq_str):
            start, end = match.span()
            nt_seq = seq[start: end]
            if strand == "-":
                start, end = n - end, n - start
            results.append(
                SeqInterval(
                    start=start, end=end, nt_seq=nt_seq,
                    type='motif', seq_id=seq_id, strand=strand
                )
            )

    find_motifs_in_strand(str(seq), strand="+")
    if include_reverse:
        if isinstance(seq, str):
            seq = Sequence(seq)
        find_motifs_in_strand(str(seq.reverse_complement()), strand="-")

    return AnalysisResult(
        results, seq_id=seq_id, type="motif", plot_func=plot_motifs,
        metadata={
            "seq_length": n,
            "sequence": str(seq)
        }
    )


def main():
    sequence = Sequence("ACTAAAGT")
    res = find_motifs(sequence, "ACT", include_reverse=True)
    print(len(res))
    res.plot(show=True)


if __name__ == "__main__":
    main()
