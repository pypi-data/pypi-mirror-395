from omibio.sequence.sequence import Sequence
from collections import Counter
from omibio.sequence.seq_utils.complement import reverse_complement

VALID_BASES = {
    "A", "T", "C", "G", "U",
    "N", "R", "Y", "K", "M", "B", "V", "D", "H", "S", "W"
}


def kmer(
    seq: Sequence | str,
    k: int, canonical: bool = False,
    min_count: int = 1,
    strict: bool = False
) -> dict[str, int]:

    if canonical:
        cache: dict[str, str] = {}

        def get_canonical(kmer_seq):
            if kmer_seq in cache:
                return cache[kmer_seq]
            rc = reverse_complement(kmer_seq, as_str=True)
            canon = min(kmer_seq, rc)
            cache[kmer_seq] = cache[rc] = canon
            return canon
    else:
        def get_canonical(kmer_seq):
            return kmer_seq

    if not isinstance(seq, (Sequence, str)):
        raise TypeError(
            "kmer() argument 'seq' must be Sequence or str, got "
            + type(seq).__name__
        )
    if not isinstance(k, int):
        raise TypeError(
            f"kmer() argument 'k' must be int, got {type(k).__name__}"
        )
    if not isinstance(min_count, int):
        raise TypeError(
            "kmer() argument 'min_count' must be int, got "
            + type(min_count).__name__
        )
    if k <= 0:
        raise ValueError(
            f"kmer() argument 'k' must be a positive number, got {k}"
        )
    if min_count < 0:
        raise ValueError(
            "kmer() argument 'min_count' must be a non-negative number, got "
            + str(min_count)
        )

    seq_str = str(seq).upper()
    n = len(seq_str)

    if strict:
        if invalid := set(seq_str) - VALID_BASES:
            raise ValueError(
                f"(Strict Mode) Invalid base(s) found: {invalid}"
            )

    if k > n:
        return Counter()

    kmer_counter: dict = Counter()

    for i in range(n - k + 1):
        curr_kmer = seq_str[i: i+k]
        kmer_counter[get_canonical(curr_kmer)] += 1

    if min_count > 1:
        kmer_counter = Counter(
            {kmer: c for kmer, c in kmer_counter.items() if c >= min_count}
        )
    return kmer_counter


def main():
    from omibio.io import read_fasta
    seq = read_fasta(r"./examples/data/example_single_long_seq.fasta")["example"]
    print(kmer(seq, 3, min_count=150))


if __name__ == "__main__":
    main()
