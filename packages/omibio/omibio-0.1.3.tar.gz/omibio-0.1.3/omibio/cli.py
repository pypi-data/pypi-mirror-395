import click
from omibio.io import read_fasta, write_fasta
from omibio.sequence import Polypeptide


@click.group()
def cli():
    """A lightweight and easy-to-use python bioinformatics toolkit."""
    pass


@cli.command()
@click.argument("fasta_file", type=click.Path(exists=True))
def gc(fasta_file: str) -> None:
    """Calculate the GC content of a sequence from a FASTA file."""

    seqs = read_fasta(fasta_file, strict=False).seq_dict()
    for name, seq in seqs.items():
        if isinstance(seq, Polypeptide):
            raise TypeError(
                "Cannot calculate gc for amino acid sequences"
            )
        gc_val = seq.gc_content(percent=True)
        click.echo(f"{name}\t{gc_val}")


@cli.command()
@click.argument("fasta_file", type=click.Path(exists=True))
@click.option(
    "--min-length",
    type=int,
    default=100,
    help="Minimum length of ORFs to consider. Defaults to 0."
)
@click.option(
    "--max-length",
    type=int,
    default=10000,
    help="Maximum length of ORFs to consider. Defaults to 10000."
)
@click.option(
    "--start-codons",
    type=str,
    default="ATG",
    help="Comma-separated start codons (e.g., ATG,GTG). Default: ATG."
)
@click.option(
    "--overlap",
    is_flag=True,
    help="Whether to allow overlapping ORFs."
)
@click.option(
    "--no-reverse",
    is_flag=True,
    help="Whether to include reverse strand ORFs."
)
@click.option(
    "--no-sort",
    is_flag=True,
    help="Whether to sort the results by length in descending order."
)
@click.option(
    "--translate", "-t",
    is_flag=True,
    help=(
        "Whether to translate nucleotide sequences to amino acid sequences."
        " (shown only if --show-seq is used)."
    )
)
@click.option(
    "--show-seq",
    is_flag=True,
    help="Whether to show orf sequence."
)
def orf(
    fasta_file: str,
    min_length: int,
    max_length: int,
    overlap: bool,
    no_reverse: bool,
    no_sort: bool,
    translate: bool,
    start_codons: str,
    show_seq: bool
) -> None:
    """Find orfs of a sequence from a FASTA file."""
    from omibio.analysis.find_orfs import find_orfs

    start_codon_set = {
        codon.strip().upper() for codon in start_codons.split(",")
    }

    seqs = read_fasta(fasta_file, strict=False).seq_dict()
    all_orfs = []

    for seq_id, seq_obj in seqs.items():
        if isinstance(seq_obj, Polypeptide):
            raise TypeError(
                "Cannot find ORFs in amino acid sequences"
            )
        orfs = find_orfs(
            seq=seq_obj,
            min_length=min_length,
            max_length=max_length,
            overlap=overlap,
            include_reverse=not no_reverse,
            sort_by_length=not no_sort,
            translate=translate,
            start_codons=start_codon_set,
            seq_id=seq_id
        )
        all_orfs.extend(orfs.intervals)

    if not no_sort:
        all_orfs.sort(key=lambda x: x.length, reverse=True)

    res: list[list[str | None]] = [
        ["sequence-name", "start", "end", "strand", "frame", "length"]
    ]

    for orf in all_orfs:
        frame = f"{orf.frame:+}" if orf.frame > 0 else orf.frame
        base_fields = [
            orf.seq_id,
            str(orf.start),
            str(orf.end),
            orf.strand,
            str(frame),
            str(orf.length)
        ]
        if show_seq:
            nt_seq = orf.nt_seq
            aa_seq = str(orf.aa_seq) if orf.aa_seq is not None else ""
            base_fields.extend([nt_seq, aa_seq])
        res.append(base_fields)

    for base_fields in res:
        click.echo("\t".join(str(f) for f in base_fields))
    click.echo(f"Total: {len(res) - 1} ORFs found")


@cli.command()
@click.argument("output", type=str)
@click.option(
    "-n", "--number",
    type=int,
    default=1,
    help="Number of random sequences to generate (default: 1)."
)
@click.option(
    "-p", "--prefix",
    type=str,
    default="random_seq",
    help="Prefix for sequence IDs (default: 'random_seq')."
)
@click.option(
    "-l", "--length",
    type=int,
    default=100,
    help="Length of sequences"
)
@click.option(
    "--alphabet",
    type=str,
    default="ATGC",
    help="Alphabet to sample from (default: ATGC)."
)
@click.option(
    "--seed",
    type=int,
    help="Random seed for reproducibility."
)
def random_fasta(
    output: str,
    length: int,
    number: int,
    prefix: str,
    alphabet: str,
    seed: int | None
) -> None:
    """Generate random nucleotide sequence(s) and output in FASTA format."""
    from omibio.sequence.seq_utils.random_seq import random_fasta as r_f

    r_f(
        file_path=output, seq_num=number, length=length,  alphabet=alphabet,
        prefix=prefix, seed=seed
    )
    click.echo(f"Success: file writed to {output}")


@cli.command()
@click.argument("fasta_file", type=click.Path(exists=True))
@click.option(
    "--name-policy",
    type=str,
    default="keep",
    help=(
        "Control the clean behavior of sequence names: \n"
        "'keep', 'id_only, 'underscores'"
    )
)
@click.option(
    "-o", "--output",
    type=click.Path(),
    required=True,
    help="Output file path."
)
@click.option(
    "--gap-policy",
    type=str,
    default="keep",
    help=(
        "Control the clean behavior of gaps: \n"
        "'keep', 'remove, 'collapse'"
    )
)
@click.option(
    "--min-len",
    type=int,
    default=10,
    help="The shortest length of the sequence to be retained"
)
@click.option(
    "--max-len",
    type=int,
    default=100_000,
    help="The longest length of the sequence to be retained"
)
@click.option(
    "--allowed-bases", "-ab",
    type=str,
    default="ATCGUNRYKMBVDHSW",
    help="Allowed bases to exist in the sequence."
)
@click.option(
    "--strict", "-s",
    is_flag=True,
    help="Whether to be strict to invalid bases."
)
@click.option(
    "--preserve-cases", "-pc",
    is_flag=True,
    help="Whether to preserve case in sequences."
)
@click.option(
    "--remove-illegal", "-ri",
    is_flag=True,
    help="Whether to remove illegal bases in non-strict mode."
)
@click.option(
    "--remove-empty", "-re",
    is_flag=True,
    help="Whether to remove sequences containing only 'N' or '-'."
)
def clean(
    fasta_file: str,
    name_policy,
    gap_policy,
    strict: bool,
    min_len: int,
    max_len: int,
    preserve_cases: bool,
    remove_illegal: bool,
    allowed_bases: str,
    remove_empty: bool,
    output: str
):
    """
    Perform data cleanup on the specified FASTA file
    and output the results to the specified file.
    """
    from omibio.sequence.seq_utils.clean import clean as c_f

    seqs = read_fasta(fasta_file, strict=False).seq_dict()
    res = c_f(
        seqs,
        name_policy=name_policy,
        gap_policy=gap_policy,
        strict=strict,
        min_len=min_len,
        max_len=max_len,
        normalize_case=not preserve_cases,
        remove_empty=remove_empty,
        remove_illegal=remove_illegal,
        allowed_bases=set(allowed_bases),
        report=False
    )
    if isinstance(res, tuple):
        cleaned, _ = res
    else:
        cleaned = res
    write_fasta(output, cleaned, space_between=True)
    click.echo(f"Success: file writed to {output}")


@cli.command()
@click.argument("fasta_file", type=click.Path(exists=True))
@click.option(
    "-o", "--output",
    type=click.Path(),
    required=True,
    help="Output file path."
)
@click.option(
    "--seed",
    type=int,
    required=True,
    help="Output file path."
)
def shuffle(
    fasta_file: str,
    output: str,
    seed: int
):
    """
    Shuffle the sequences in the FASTA file
    and output them to the specified file.
    """
    from omibio.sequence.seq_utils.shuffle_seq import shuffle_seq
    import random

    res = {}
    rng = random.Random(seed)

    seqs = read_fasta(fasta_file, strict=False).seq_dict()

    for name, seq in seqs.items():
        seq_seed = rng.randint(0, 2**32 - 1)
        shuffled = shuffle_seq(seq, seed=seq_seed, as_str=True)
        res[name] = shuffled

    write_fasta(output, res, space_between=True)
    click.echo(f"Success: file writed to {output}")


if __name__ == "__main__":
    cli()
