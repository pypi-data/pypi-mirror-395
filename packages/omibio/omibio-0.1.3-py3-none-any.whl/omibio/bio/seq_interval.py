from dataclasses import dataclass
from omibio.sequence.sequence import Sequence
from omibio.sequence.polypeptide import Polypeptide


@dataclass(frozen=True)
class SeqInterval:
    """
    Stores information about the sequence range.
    """

    start: int
    end: int

    nt_seq: str | None = None

    type: str | None = None
    seq_id: str | None = None
    strand: str = "+"
    gc: float | None = None

    aa_seq: str | None = None
    frame: int = 0

    def __post_init__(self):
        if (
            self.nt_seq is not None
            and not isinstance(self.nt_seq, (str, Sequence))
        ):
            raise TypeError(
                "SeqInterval argument 'nt_seq' can only take either str "
                f"or Sequence as input, got {type(self.nt_seq).__name__}"
            )
        if isinstance(self.nt_seq, Sequence):
            object.__setattr__(self, 'nt_seq', str(self.nt_seq))

        if (
            self.aa_seq is not None
            and not isinstance(self.aa_seq, (Polypeptide, str))
        ):
            raise TypeError(
                "SeqInterval argument 'aa_seq' an only take either str"
                f"or Polypeptide as input, got {type(self.aa_seq).__name__}"
            )
        if isinstance(self.aa_seq, Polypeptide):
            object.__setattr__(self, 'aa_seq', str(self.aa_seq))

        if self.strand not in {"+", "-"}:
            raise ValueError(f"strand must be '+' or '-', got {self.strand!r}")
        if self.start < 0 or self.end < 0:
            raise ValueError("start and end must be non-negative integers")
        if self.start > self.end:
            raise ValueError(
                f"Invalid interval: start ({self.start}) > end ({self.end})"
            )
        if self.gc is not None and not isinstance(self.gc, float):
            raise TypeError(
                "SeqInterval argument 'vc' must be float, "
                f"got {type(self.gc).__name__}"
            )

    @property
    def length(self) -> int:
        return self.end - self.start

    def to_sequence(
        self, rna: bool | None = None, strict: bool = False
    ) -> Sequence:
        """Returns the nucleotide sequence as a Sequence object."""

        if self.nt_seq is not None:
            return Sequence(self.nt_seq, rna=rna, strict=strict)
        else:
            raise ValueError(
                "Cannot create Sequence: nt_seq is not set. "
            )

    def to_polypeptide(self, strict: bool = False) -> Polypeptide:
        """Returns the amino acid sequence as a Polypeptide object."""

        if self.aa_seq is not None:
            return Polypeptide(self.aa_seq, strict=strict)
        else:
            raise ValueError(
                "Cannot create Polypeptide: aa_seq is not set. "
            )

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        from omibio.utils.truncate_repr import truncate_repr
        seq_repr = truncate_repr(self.nt_seq)
        info = (
            f"SeqInterval({seq_repr}, "
            f"{self.start}-{self.end}({self.strand}), "
            f"length={self.length}"
        )
        extras = []

        if self.type is not None:
            extras.append(f"type={self.type!r}")
        if self.seq_id is not None:
            extras.append(f"seq_id={self.seq_id!r}")

        if self.aa_seq is not None:
            aa_seq_repr = truncate_repr(self.aa_seq)
            extras.append(f"aa_seq={aa_seq_repr}")
        if self.frame != 0:
            extras.append(f"frame={self.frame}")

        if extras:
            info += ", " + ", ".join(extras)

        return info + ")"

    def __str__(self):
        return self.nt_seq if self.nt_seq else ""


def main():
    seq = SeqInterval(
        start=0, end=12,
        nt_seq='ATGAAAAAATAA',
        seq_id='a',
        aa_seq="MKK",
        type="ORF",
        frame=1
    )
    print(repr(seq))


if __name__ == "__main__":
    main()
