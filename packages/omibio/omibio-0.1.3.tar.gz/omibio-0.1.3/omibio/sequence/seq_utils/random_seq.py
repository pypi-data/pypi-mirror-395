import random
from omibio.sequence import Sequence, Polypeptide
from omibio.io.write_fasta import write_fasta


def random_seq(
    length: int,
    alphabet: str = "ATCG",
    weights: list[float] | None = None,
    seed: int | None = None,
    as_str: bool = False,
    as_polypeptide: bool = False,
    seq_strict: bool = False
) -> Sequence | str | Polypeptide:
    """Generate a random sequence.

    Args:
        length (int):
            Length of the sequence to generate.
        alphabet (str, optional):
            Alphabet to sample from. Defaults to "ATCG".
        weights (list[float] | None, optional):
            Weights for each character in the alphabet. Defaults to None.
        seed (int | None, optional):
            Random seed for reproducibility. Defaults to None.
        as_str (bool, optional):
            If True, return the sequence as a string. Defaults to False.
        seq_strict (bool, optional):
            If True and as_str is False, create a Sequence object in strict
            mode. Defaults to False.

    Raises:
        ValueError: length must be a non-negative integer
        ValueError: Alphabet cannot be empty
        ValueError: Length of 'weights' must match length of 'alphabet'

    Returns:
        Sequence | str: The generated random sequence.
    """

    if length < 0:
        raise ValueError(
            f"Length must be a non-negative integer, got {length}"
        )

    if not alphabet:
        raise ValueError("Alphabet cannot be empty")

    if weights is not None:
        if len(weights) != len(alphabet):
            raise ValueError(
                "Length of 'weights' must match length of 'alphabet'"
            )

    rng = random.Random(seed)

    if weights is not None:
        seq = "".join(rng.choices(alphabet, weights, k=length))
    else:
        seq = "".join(rng.choices(alphabet, k=length))

    if as_polypeptide:
        return Polypeptide(seq, strict=seq_strict)

    return seq if as_str else Sequence(seq, strict=seq_strict)


def random_fasta(
    file_path: str,
    seq_num: int,
    length: int,
    alphabet: str = "ATCG",
    prefix: str = "Sequence",
    weights: list[float] | None = None,
    seed: int | None = None,
) -> None:
    """Generate a FASTA file containing a random sequence.

    Args:
        file_path (str):
            Path to the output FASTA file.
        seq_num (int):
            Number of sequences to generate.
        length (int):
            Length of each sequence.
        alphabet (str, optional):
            Alphabet to sample from. Defaults to "ATCG".
        prefix (str, optional):
            Prefix for sequence IDs. Defaults to "Sequence".
        weights (list[float] | None, optional):
            Weights for each character in the alphabet. Defaults to None.
        seed (int | None, optional):
            Random seed for reproducibility. Defaults to None.
    """

    rng = random.Random(seed)
    seq_dict = {}

    for i in range(1, seq_num+1):
        seq_seed = rng.randint(0, 2**32 - 1)
        seq_dict[f"{prefix}_{i}"] = random_seq(
            length=length, alphabet=alphabet,
            weights=weights, as_str=True, seed=seq_seed
        )
    write_fasta(file_name=file_path, seq_dict=seq_dict, space_between=True)


def main():
    output_path = r"./examples/data/random.fasta"
    random_fasta(output_path, 30, 2000)
    print(output_path)


if __name__ == "__main__":
    main()
