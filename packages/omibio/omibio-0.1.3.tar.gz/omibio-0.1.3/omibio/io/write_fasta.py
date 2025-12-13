from pathlib import Path
from omibio.sequence import Sequence, Polypeptide


def write_fasta(
    file_name: str,
    seq_dict: dict[str, Sequence | Polypeptide | str],
    line_len: int = 60,
    space_between: bool = False
) -> list[str]:
    """Writes sequences to a FASTA file.

    Args:
        file_name (_type_):
            Path to output FASTA file.
        seq_dict (_type_):
            Dictionary of sequence name (str) to sequence (str or Sequence).
        line_len (int, optional):
            Number of characters per line in the FASTA file. Defaults to 60.
        space_between (bool, optional):
            Whether to add a blank line between sequences. Defaults to False.

    Raises:
        TypeError:
            if seq_dict is not a dict or if sequence names are not str.
        OSError:
            if unable to write to file.
    """
    if not seq_dict:
        return []
    if not isinstance(seq_dict, dict):
        raise TypeError(
            "write_fasta() argument 'seq_dict' must be dict, got "
            + type(seq_dict).__name__
        )
    file_path = Path(file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    try:
        with file_path.open("w", encoding="utf-8") as f:
            for name, seq in seq_dict.items():
                if not isinstance(name, str):
                    raise TypeError(
                        "write_fasta() Sequence name must be str, got "
                        + type(name).__name__
                    )

                seq = str(seq).replace("\n", "")
                f.write(f">{name}\n")
                lines.append(f">{name}")

                for i in range(0, len(seq), line_len):
                    f.write(seq[i:i+line_len] + "\n")
                    lines.append(seq[i:i+line_len])

                if space_between:
                    f.write("\n")

    except OSError as e:
        raise OSError(f"Could not write FASTA to '{file_name}': {e}") from e

    return lines


def main():
    from omibio.io.read_fasta import read_fasta

    input_path = r"./examples/data/example_short_seqs.fasta"
    output_path = r"./examples/output/write_fasta_output.fasta"

    seq_dict = read_fasta(input_path).seq_dict()
    lines = write_fasta(output_path, seq_dict, space_between=True)
    print(output_path)
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
