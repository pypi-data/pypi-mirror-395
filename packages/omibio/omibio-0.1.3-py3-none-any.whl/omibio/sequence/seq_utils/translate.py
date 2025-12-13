from omibio.sequence.sequence import Sequence
from omibio.sequence.polypeptide import Polypeptide
from omibio.bio.seq_interval import SeqInterval


DNA_CODON_TABLE = {
    'TTT': 'F', 'TTC': 'F',  # Phenylalanine
    'TTA': 'L', 'TTG': 'L',  # Leucine
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',  # Serine
    'TAT': 'Y', 'TAC': 'Y',  # Tyrosine
    'TAA': '*', 'TAG': '*',  # Stop codons
    'TGT': 'C', 'TGC': 'C',  # Cysteine
    'TGA': '*',              # Stop codon
    'TGG': 'W',              # Tryptophan

    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',  # Leucine
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',  # Proline
    'CAT': 'H', 'CAC': 'H',  # Histidine
    'CAA': 'Q', 'CAG': 'Q',  # Glutamine
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',  # Arginine

    'ATT': 'I', 'ATC': 'I', 'ATA': 'I',  # Isoleucine
    'ATG': 'M',                          # Methionine (Start)
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',  # Threonine
    'AAT': 'N', 'AAC': 'N',  # Asparagine
    'AAA': 'K', 'AAG': 'K',  # Lysine
    'AGT': 'S', 'AGC': 'S',  # Serine
    'AGA': 'R', 'AGG': 'R',  # Arginine

    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',  # Valine
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',  # Alanine
    'GAT': 'D', 'GAC': 'D',  # Aspartic acid
    'GAA': 'E', 'GAG': 'E',  # Glutamic acid
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',  # Glycine
}


def translate_nt(
    seq: Sequence | str | SeqInterval | None,
    strict: bool = False,
    as_str: bool = False,
    stop_symbol: bool = False,
    to_stop: bool = False,
    frame: int = 0,
    require_start: bool = False
) -> Polypeptide | str:
    """Translate a nucleotide sequence to an amino acid sequence.

    Args:
        seq (Sequence | str):
            Input nucleotide sequence.
        stop_symbol (bool, optional):
            Whether to include stop codon symbol '*'. Defaults to True.
        to_stop (bool, optional):
            Whether to stop translation at the first stop codon.
            Defaults to False.
        frame (int, optional):
            Frame offset (0, 1, or 2). Defaults to 0.
        require_start (bool, optional):
            Whether to start translation at the first start codon.
            Defaults to False.

    Raises:
        ValueError: If frame is not 0, 1, or 2.

    Returns:
        str: Translated amino acid sequence.
    """
    if not isinstance(seq, (Sequence, str, SeqInterval)):
        raise TypeError(
            "find_otranslaterfs() argument 'seq' must be Sequence or str, not "
            + type(seq).__name__
        )

    if not seq or len(seq) < 3:
        return ""

    if frame not in (0, 1, 2):
        raise ValueError(f"Invalid frame: {frame}, Frame must be 0, 1, or 2.")

    aa_seq = []
    start_idx = 0
    seq = str(seq).replace("U", "T")
    seq = seq[frame:]

    if require_start:
        for j in range(0, len(seq) - 2, 3):
            if seq[j: j+3] == "ATG":
                start_idx = j
                break
        else:
            return ""

    for i in range(start_idx, len(seq) - 2, 3):
        codon = seq[i: i + 3]
        amino = DNA_CODON_TABLE.get(codon, "X")

        if amino == "*":
            if stop_symbol:
                aa_seq.append("*")
            if to_stop:
                break
            continue

        aa_seq.append(amino)

    res = "".join(aa_seq)

    return res if as_str else Polypeptide(res, strict=strict)


def main() -> None:
    from omibio.io import read_fasta
    seq = read_fasta("./examples/data/e_coil_gene_sequence.fasta").seqs()[0]
    aa = translate_nt(
        seq, stop_symbol=True, to_stop=True, require_start=True, frame=2
    )
    print(str(aa))


if __name__ == "__main__":
    main()
