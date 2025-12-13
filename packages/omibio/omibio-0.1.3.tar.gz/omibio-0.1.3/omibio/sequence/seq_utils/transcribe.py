from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from omibio.sequence.sequence import Sequence


def transcribe(
    seq: Union["Sequence", str],
    strand: str = "+",
    as_str: bool = False
) -> Union["Sequence", str]:
    """Transcribe a DNA seq sequence to RNA.

    Args:
        seq (Sequence | str): input seq sequence
        strand (str, optional):
            Sense or antisense, either '+' or '-'. Defaults to '+'.
        as_str (bool, optional):
            Whether to return the result as a string. Defaults to False.

    Raises:
        TypeError: If the input sequence is not of type Sequence or string.

    Returns:
        Sequence | str: transcribed RNA sequence
    """
    from omibio.sequence.sequence import Sequence
    if not isinstance(seq, (Sequence, str)):
        raise TypeError(
            "transcribe() argument 'seq' must be Sequence or str, not "
            + type(seq).__name__
        )
    if isinstance(seq, str):
        seq = Sequence(seq)

    res = seq.transcribe(strand=strand)
    return str(res) if as_str else res


def reverse_transcribe(
    seq: Union["Sequence", str],
    as_str: bool = False
) -> Union["Sequence", str]:
    """Reverse transcribe a RNA seq sequence to DNA.

    Args:
        seq (Sequence | str): input seq sequence
        as_str (bool, optional):
        Whether to return the result as a string. Defaults to False.

    Raises:
        TypeError: If the input sequence is not of type Sequence or string.

    Returns:
        Sequence | str: reverse transcribed DNA sequence
    """
    from omibio.sequence.sequence import Sequence
    if not isinstance(seq, (Sequence, str)):
        raise TypeError(
            "reverse_transcribe() argument 'seq' must be Sequence or str, not "
            + type(seq).__name__
        )
    if isinstance(seq, str):
        seq = Sequence(seq)

    res = seq.reverse_transcribe()
    return str(res) if as_str else res


def main():
    print([transcribe("ACTG", strand="+")])
    print([reverse_transcribe("ACTG")])


if __name__ == "__main__":
    main()
