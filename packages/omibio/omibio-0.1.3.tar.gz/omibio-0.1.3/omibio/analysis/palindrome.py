from omibio.sequence.sequence import Sequence
from omibio.bio import SeqInterval, AnalysisResult


def find_palindrome(
    seq: Sequence | str,
    min_len: int = 4,
    max_len: int = 12,
    seq_id: str | None = None
) -> AnalysisResult:
    """Find palindromic sequences in a given sequence.

    Args:
        seq (Sequence | str):
            Input sequence to search for palindromes.
        min_len (int, optional):
            Minimum length of palindromic sequences to find. Defaults to 4.
        max_len (int, optional):
            Maximum length of palindromic sequences to find. Defaults to 12.

    Raises:
        TypeError:
            If the input sequence is not of type Sequence or string.
        TypeError:
            If min_len or max_len is not of type int.
        ValueError:
            If min_len is larger than the length of the sequence.
        ValueError:
            If min_len is larger than max_len.

    Returns:
        list[Palindrome]: List of Palindrome objects found in the sequence.
    """

    if not seq:
        return AnalysisResult(
            intervals=[], seq_id=seq_id, type="palindrome",
            metadata={
                "seq_length": 0,
                "sequence": ""
            }
        )
    if not isinstance(seq, (Sequence, str)):
        raise TypeError(
            "find_palindrome() argument 'seq' must be Sequence or str, got "
            + type(seq).__name__
        )
    if not isinstance(min_len, int) or not isinstance(max_len, int):
        raise TypeError(
            "find_palindrome() argument 'min_len' and 'max_len must be int."
        )

    n = len(seq)

    if min_len > n:
        raise ValueError(
            f"find_palindrome() argument 'min_len' {min_len}"
            f"cannot be larger than the length of sequence {n}"
        )
    if max_len < min_len:
        raise ValueError(
            f"find_palindrome() argument 'min_len' {min_len} "
            f"cannot be larger than 'max_len' {max_len}"
        )

    if isinstance(seq, str):
        seq = Sequence(seq)

    rev_seq = seq.reverse_complement()
    results = []

    start = (max_len) if max_len % 2 == 0 else (max_len - 1)

    for length in range(start, min_len - 1, -2):

        for i in range(0, n - length + 1):
            candidate = seq[i: i+length]
            if candidate == rev_seq[n-i-length: n-i]:
                results.append(
                    SeqInterval(
                        start=i, end=i+length, nt_seq=str(candidate),
                        type='palindrome'
                    )
                )

    return AnalysisResult(
        results, seq_id=seq_id, type="palindrome",
        metadata={
            "seq_length": n,
            "sequence": str(seq)
        }
    )


def main():
    seq = Sequence("GAAUUTGG")
    res = find_palindrome(seq)
    print(list(res))


if __name__ == "__main__":
    main()
