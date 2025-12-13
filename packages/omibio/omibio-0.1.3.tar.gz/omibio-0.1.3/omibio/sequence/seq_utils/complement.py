from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from omibio.sequence.sequence import Sequence


def complement(
    seq: Union["Sequence", str],
    as_str: bool = False
) -> Union["Sequence", str]:
    """Complement a given sequence.

    Args:
        seq (Sequence | str): Input sequence.
        as_str (bool, optional):
            Whether to return the result as a string. Defaults to False.

    Raises:
        TypeError: If the input sequence is not of type Sequence or string.

    Returns:
        Sequence | str: Complemented sequence.
    """
    from omibio.sequence.sequence import Sequence
    # Validate input type
    if not isinstance(seq, (Sequence, str)):
        raise TypeError(
            "complement() argument 'seq' must be Sequence or str, not "
            + type(seq).__name__
        )
    if isinstance(seq, str):
        seq = Sequence(seq)

    res = seq.complement()
    return (res.sequence if as_str is True else res)


def reverse_complement(
    seq: Union["Sequence", str],
    as_str: bool = False
) -> Union["Sequence", str]:
    """Reverse complement a given sequence.

    Args:
        seq (Sequence | str): Input sequence.
        as_str (bool, optional):
            Whether to return the result as a string. Defaults to False.

    Raises:
        TypeError: If the input sequence is not of type Sequence or string.

    Returns:
        str: Reverse complemented sequence.
    """
    from omibio.sequence.sequence import Sequence
    # Validate input type
    if not isinstance(seq, (Sequence, str)):
        raise TypeError(
            "reverse_complement() argument 'seq' must be Sequence or str, not "
            + type(seq).__name__
        )
    if isinstance(seq, str):
        seq = Sequence(seq)

    res = seq.reverse_complement()
    return str(res) if as_str is True else res


def main():
    seq = "ATGCCCTAA"
    print([complement(seq, as_str=True)])
    print([reverse_complement(seq)])


if __name__ == "__main__":
    main()
