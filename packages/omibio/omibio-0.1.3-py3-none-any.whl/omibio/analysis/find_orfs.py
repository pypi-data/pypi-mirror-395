from omibio.io.read_fasta import read_fasta
from omibio.bio import SeqInterval, AnalysisResult
from omibio.sequence import Sequence
from omibio.sequence.seq_utils.translate import translate_nt
from omibio.viz import plot_orfs

STOP_CODONS = {"TAA", "TAG", "TGA"}


def find_orfs_in_frame(
    seq: str,
    min_length: int,
    max_length: int,
    overlap: bool,
    strand: str,
    frame: int,
    translate: bool,
    start_codons: set[str],
    seq_id: str | None = None
) -> list[SeqInterval]:
    """Internal helper function. Scan a single frame and return raw ORFs."""

    orf_list = []
    active_starts: list[int] = []

    for i in range(frame, len(seq)-2, 3):
        codon = seq[i: i+3]
        if codon in STOP_CODONS:
            end_idx = i + 3

            for start_idx in active_starts:
                orf_length = i + 3 - start_idx

                if not (min_length <= orf_length <= max_length):
                    continue

                nt_seq = seq[start_idx: end_idx]
                aa_seq = (
                    str(translate_nt(nt_seq, stop_symbol=False)) if translate
                    else None
                )
                orf_list.append(
                    SeqInterval(
                        start=start_idx, end=end_idx,
                        nt_seq=nt_seq, type='ORF',
                        strand=strand, frame=frame+1,
                        aa_seq=aa_seq, seq_id=seq_id
                    )
                )
            active_starts = []
        else:
            if codon in start_codons:
                if overlap:
                    active_starts.append(i)
                else:
                    if not active_starts:
                        active_starts.append(i)

    return orf_list


def find_orfs(
    seq: Sequence | str,
    min_length: int = 100,
    max_length: int = 10000,
    overlap: bool = False,
    include_reverse: bool = True,
    sort_by_length: bool = True,
    translate: bool = False,
    start_codons: set[str] | list[str] | tuple[str] = {"ATG"},
    seq_id: str | None = None
) -> AnalysisResult:
    """Find ORFs in a given sequence.

    Args:
        seq (Sequence | str):
            Input sequence.
        min_length (int, optional):
            Minimum length of ORFs to consider. Defaults to 100.
        max_length (int, optional):
            Maximum length of ORFs to consider. Defaults to 10000.
        overlap (bool, optional):
            Whether to allow overlapping ORFs. Defaults to False.
        include_reverse (bool, optional):
            Whether to include reverse strand ORFs. Defaults to True.
        sort_by_length (bool, optional):
            Whether to sort the results by length in descending order.
            Defaults to True.
        translate (bool, optional):
            Whether to translate the nucleotide sequences to amino acid
            sequences. Defaults to False.
        start_codons (set[str], optional):
            Set of start codons to consider. Defaults to {"ATG"}.
        seq_id (str | None, optional):
            Identifier for the sequence. Defaults to None.

    Returns:
        AnalysisResult:
            ORF analysis result object.

    Raises:
        TypeError:
            If input types are incorrect.
        ValueError:
            If input value 'min_length' is negative or 'start_codons' is empty.
    """

    # Type and value validation

    # Input: seq
    if not isinstance(seq, (Sequence, str)):
        raise TypeError(
            "find_orfs() argument 'seq' must be Sequence or str, not "
            + type(seq).__name__
        )
    # Input: min_length & max_length
    if not isinstance(min_length, int):
        raise TypeError(
            "find_orfs() argument 'min_length' must be a non-negative integer"
        )
    if min_length < 0:
        raise ValueError(
            "find_orfs() argument 'min_length' must be non-negative, got "
            + str(min_length)
        )
    if not isinstance(max_length, int):
        raise TypeError(
            "find_orfs() argument 'max_length' must be a non-negative integer"
        )
    if max_length < 0:
        raise ValueError("max_length must be non-negative")
    if max_length < min_length:
        raise ValueError("max_length must be >= min_length")
    # Input: start_codons
    if not start_codons:
        raise ValueError("start_codons cannot be empty")
    validated_start_codons = set()
    for codon in start_codons:
        if not isinstance(codon, str):
            raise TypeError(
                "find_orfs() argument 'start_codons' must contains str , got "
                + type(codon).__name__
            )
        if len(codon) != 3:
            raise ValueError(
                f"Start codon '{codon}' must be exactly 3 nucleotides long"
            )
        codon_upper = codon.upper().replace('U', 'T')
        validated_start_codons.add(codon_upper)
    # Input: seq_id
    if seq_id is not None and not isinstance(seq_id, str):
        raise TypeError(
            "find_orfs() argument 'seq_id' must be str, not "
            + type(seq_id).__name__
        )

    if isinstance(seq, str):
        seq = Sequence(seq, strict=False)
    if seq.is_rna is True:
        seq = seq.reverse_transcribe()

    seq_length = len(seq)
    results = []

    for frame in (0, 1, 2):
        results.extend(
            find_orfs_in_frame(
                seq.sequence, min_length=min_length, max_length=max_length,
                overlap=overlap, strand='+', frame=frame, translate=translate,
                start_codons=validated_start_codons, seq_id=seq_id
            )
        )

    if include_reverse:
        rev_seq = seq.reverse_complement()
        for frame in (0, 1, 2):
            rev_orfs = find_orfs_in_frame(
                rev_seq.sequence, min_length=min_length, max_length=max_length,
                overlap=overlap, strand='-', frame=frame, translate=translate,
                start_codons=validated_start_codons, seq_id=seq_id
                )
            for orf in rev_orfs:
                results.append(
                    SeqInterval(
                        start=seq_length - orf.end,
                        end=seq_length - orf.start,
                        nt_seq=orf.nt_seq, type='ORF',
                        strand='-', frame=-(frame + 1),
                        aa_seq=orf.aa_seq, seq_id=seq_id
                    )
                )

    if sort_by_length:
        results.sort(key=lambda orf: orf.length, reverse=True)

    return AnalysisResult(
        intervals=results,
        seq_id=seq_id,
        plot_func=plot_orfs, type="ORF",
        metadata={
            "seq_length": seq_length,
            "sequence": str(seq)
        }
    )


def main():
    seqs = read_fasta(r"./examples/data/example_single_long_seq.fasta")
    sequence = seqs["example"]
    res = find_orfs(sequence, translate=True, seq_id='example')
    ax = plot_orfs(res)
    ax.figure.show()


if __name__ == "__main__":
    main()
