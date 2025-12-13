from omibio.sequence.polypeptide import Polypeptide


class Sequence:
    """
    A class representing a DNA or RNA sequence with methods for analysis.
    """

    _VALID_DNA_BASES = {
        "A", "T", "C", "G",
        "N", "R", "Y", "K", "M", "B", "V", "D", "H", "S", "W"
    }
    _VALID_RNA_BASES = {
        "A", "U", "C", "G",
        "N", "R", "Y", "K", "M", "B", "V", "D", "H", "S", "W"
    }

    def __init__(
        self,
        sequence: str | None = None,
        rna: bool | None = None,
        strict: bool = False
    ):
        """Initialize a Sequence object.

        Args:
            sequence (str | None, optional):
                The nucleotide sequence as a string. Defaults to None.
            rna (bool | None, optional):
                Indicates if the sequence is RNA (True), DNA (False),
                or unknown (None). Defaults to None.
            strict (bool, optional):
                If True, enables strict mode for validation. Defaults to False.

        Raises:
            TypeError: If rna is not bool or None
            TypeError: If strict is not bool
        """

        if rna is not None and not isinstance(rna, bool):
            raise TypeError(
                "Sequence argument 'rna' must be bool or None, got "
                + type(rna).__name__
            )
        if not isinstance(strict, bool):
            raise TypeError(
                "Sequence argument 'strict' must be bool or None, got "
                + type(strict).__name__
            )
        self._is_rna = rna
        self._strict = strict
        self.sequence = sequence if sequence is not None else ""

    @property
    def strict(self) -> bool:
        """Getter, returns whether strict mode is enabled."""
        return self._strict

    @property
    def is_rna(self) -> bool | None:
        """Getter, returns whether the sequence is RNA (True), DNA (False),
        or unknown (None).
        """
        return self._is_rna

    @property
    def type(self) -> str:
        """Return 'DNA' or 'RNA' indicating the sequence type."""
        return "RNA" if self._is_rna else "DNA"

    @property
    def sequence(self) -> str:
        """Getter, returns the sequence."""
        return self._sequence

    @sequence.setter
    def sequence(self, sequence: str) -> None:
        """Setter, based on the strict rule, performs a sequence base validity
        check and automatically determines the DNA/RNA type.

        Args:
            sequence (str): The nucleotide sequence.

        Raises:
            TypeError:
                if sequence is not str
            ValueError:
                If strict mode is enabled and invalid bases are found
            ValueError:
                If strict mode is enabled and both 'T' and 'U' are found
        """
        if sequence is None:
            sequence = ""
        elif not isinstance(sequence, str):
            raise TypeError(
                "Sequence argument 'sequence' must be str, not "
                + type(sequence).__name__
            )

        sequence = sequence.upper()  # Convert to uppercase

        if self._strict:
            if self._is_rna is None:
                contains_t = "T" in sequence
                contains_u = "U" in sequence
                if contains_t and contains_u:
                    raise ValueError(
                        "(Strict Mode) "
                        "Ambiguous sequence: contains both 'T' and 'U'"
                    )
                valid_bases = (
                    self._VALID_RNA_BASES if contains_u
                    else self._VALID_DNA_BASES
                )
            else:
                valid_bases = (
                    self._VALID_RNA_BASES if self._is_rna
                    else self._VALID_DNA_BASES
                )

            if invalid := set(sequence) - valid_bases:
                seq_typ = (
                    "RNA" if valid_bases == self._VALID_RNA_BASES else "DNA"
                )
                # Validate sequence contains only A, C, G, T，N
                raise ValueError(
                    f"(Strict Mode) Invalid base(s) for {seq_typ} "
                    f"sequence found: {invalid}"
                )

        self._sequence = sequence

        if self._is_rna is None:
            self._is_rna = "U" in sequence

    def gc_content(self, percent: bool = False) -> float | str:
        """Calculate and return the GC content of the sequence."""
        seq_length = len(self.sequence)
        if seq_length == 0:
            return 0.0 if not percent else "0.00%"

        gc = self.sequence.count("G") + self.sequence.count("C")

        return (round(gc / seq_length, 4) if not percent
                else f"{(gc / seq_length) * 100:.2f}%")

    def complement(self) -> "Sequence":
        """Return the complement of the sequence."""
        if self._is_rna is True:
            comp_table = str.maketrans("AUCGRYKMBVDHSWN", "UAGCYRMKVBHDSWN")
        else:
            comp_table = str.maketrans("ATCGRYKMBVDHSWN", "TAGCYRMKVBHDSWN")
        comp = self.sequence.translate(comp_table)
        return Sequence(comp, rna=self._is_rna, strict=self._strict)

    def reverse_complement(self) -> "Sequence":
        """Return the reverse complement of the sequence."""
        if self._is_rna is True:
            rev_comp_tb = str.maketrans("AUCGRYKMBVDHSWN", "UAGCYRMKVBHDSWN")
        else:
            rev_comp_tb = str.maketrans("ATCGRYKMBVDHSWN", "TAGCYRMKVBHDSWN")
        rev_comp = self.sequence.translate(rev_comp_tb)[::-1]
        return Sequence(rev_comp, rna=self._is_rna, strict=self._strict)

    def transcribe(self, strand: str = "+") -> "Sequence":
        """Transcribe the DNA sequence to RNA."""
        if self._is_rna is True:
            return self
        if strand not in {"+", "-"}:
            raise ValueError("strand type should be either '+' or '-'")
        if strand == "+":
            rna_seq = self.sequence.replace("T", "U")
        else:
            rna_seq = self.reverse_complement().sequence.replace("T", "U")
        return Sequence(rna_seq, rna=True, strict=self._strict)

    def reverse_transcribe(self) -> "Sequence":
        """Transcribe the RNA sequence to DNA."""
        if self._is_rna is False:
            return self
        return Sequence(
            self.sequence.replace("U", "T"), rna=False, strict=self._strict
        )

    def subseq(self, start: int, end: int | None = None) -> "Sequence":
        """Return a subsequence from start to end (end exclusive)."""
        if (
            not isinstance(start, int)
            or (end is not None and not isinstance(end, int))
        ):
            raise TypeError("subseq() argument 'start' and ''end' must be int")
        return Sequence(
            self.sequence[start: end], rna=self._is_rna, strict=self._strict
        )

    def translate_nt(
        self,
        strict: bool = False,
        as_str: bool = False,
        stop_symbol: bool = False,
        to_stop: bool = False,
        frame: int = 0,
        require_start: bool = False
    ) -> Polypeptide | str:
        """Translate the nucleotide sequence to an amino acid sequence."""
        from omibio.sequence.seq_utils.translate import translate_nt

        return translate_nt(
            self.sequence,
            as_str=as_str,
            strict=strict,
            stop_symbol=stop_symbol,
            to_stop=to_stop,
            frame=frame,
            require_start=require_start
        )

    def count(self, base: str) -> int:
        """Count occurrences of a base in the sequence."""
        return self.sequence.count(base)

    def copy(
        self,
        as_rna: bool | None = None,
        strict: bool | None = None
    ) -> "Sequence":
        """Return a copy of the Sequence object."""

        new_strict = strict if strict is not None else self.strict
        return Sequence(str(self), rna=as_rna, strict=new_strict)

    def to_strict(self, as_rna: bool | None = None) -> "Sequence":
        """Return a copy of the Sequence object in strict mode."""
        return self.copy(as_rna=as_rna, strict=True)

    def is_valid(self) -> bool:
        """Check if the sequence contains only valid bases."""
        valid_bases = (
            self._VALID_RNA_BASES if self._is_rna
            else self._VALID_DNA_BASES
        )
        return not (set(self.sequence) - valid_bases)

    def __len__(self) -> int:
        """Return the length of the sequence."""
        return len(self.sequence)

    def __str__(self) -> str:
        """Return string representation of the sequence."""
        return self.sequence

    def __repr__(self) -> str:
        from omibio.utils.truncate_repr import truncate_repr
        seq_repr = truncate_repr(self.sequence)
        return (
            f"Sequence({seq_repr}, "
            f"type={self.type}, "
            f"strict={self._strict})"
        )

    def __getitem__(self, idx) -> str:
        return self.sequence[idx]

    def __setitem__(self, idx: int, new_base: str) -> None:
        seq_list = list(self.sequence)
        seq_list[idx] = new_base
        self.sequence = "".join(seq_list)

    def __iter__(self):
        return iter(self.sequence)

    def __contains__(self, item) -> bool:
        return item in self.sequence

    def __eq__(self, other) -> bool:
        if isinstance(other, Sequence):
            if self._strict or other.strict:
                return (
                    self.sequence == other.sequence
                    and self._is_rna == other.is_rna
                )
            else:
                return self.sequence == other.sequence

        elif isinstance(other, str):
            return self.sequence == other.upper()
        return False

    def __add__(self, other) -> "Sequence":
        if isinstance(other, Sequence):
            strict_mode = self._strict or other.strict
            if strict_mode and self._is_rna != other.is_rna:
                raise TypeError(
                    "(Strict Mode) "
                    "Cannot combine RNA sequence and DNA sequence"
                )
            rna_result = self._is_rna
            return Sequence(
                self.sequence + other.sequence,
                rna=rna_result, strict=strict_mode
            )

        elif isinstance(other, str):
            other = other.upper()
            if self._strict:
                if "U" in other and "T" in other:
                    raise ValueError(
                        "(Strict Mode) Invalid string added to Sequence: "
                        "contains both 'U' and 'T'"
                    )
                if (
                    (("U" in other) and not self._is_rna)
                    or (("T" in other) and self._is_rna)
                ):
                    raise TypeError(
                        "(Strict Mode) "
                        "Cannot combine RNA sequence and DNA sequence"
                    )
            return Sequence(
                self.sequence + other, rna=self._is_rna, strict=self._strict
            )

        else:
            raise TypeError(
                "Can only add Sequence or str to Sequence, got "
                + type(other).__name__
            )

    def __mul__(self, n: int) -> "Sequence":
        if not isinstance(n, int):
            raise TypeError(
                f"Can only multiply by int, got {type(n).__name__}"
            )
        if n < 0:
            raise ValueError(
                "Sequence cannot be multiply by a negative number"
            )

        return Sequence(
            self.sequence * n, rna=self._is_rna, strict=self._strict
        )


def main():
    dna = Sequence("AAAATGCATGCTGACTGTAGCTGATTTATTGCTATC")
    dna2 = dna.copy()
    print(dna == dna2)


if __name__ == "__main__":
    main()
