from collections import Counter, defaultdict


class Polypeptide:

    VALID_AA = {
        "A", "R", "N", "D", "C", "Q", "E", "G", "H", "I",
        "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V",
    }

    AA_MASS = {
        "A": 71.03711, "C": 103.00919, "D": 115.02694, "E": 129.04259,
        "F": 147.06841, "G": 57.02146, "H": 137.05891, "I": 113.08406,
        "K": 128.09496, "L": 113.08406, "M": 131.04049, "N": 114.04293,
        "P": 97.05276, "Q": 128.05858, "R": 156.10111, "S": 87.03203,
        "T": 101.04768, "V": 99.06841, "W": 186.07931, "Y": 163.06333,
    }

    RESIDUE_FORMULA = {
        "A": {"C": 3, "H": 5, "N": 1, "O": 1},
        "R": {"C": 6, "H": 12, "N": 4, "O": 1},
        "N": {"C": 4, "H": 6, "N": 2, "O": 2},
        "D": {"C": 4, "H": 5, "N": 1, "O": 3},
        "C": {"C": 3, "H": 5, "N": 1, "O": 1, "S": 1},
        "E": {"C": 5, "H": 7, "N": 1, "O": 3},
        "Q": {"C": 5, "H": 8, "N": 2, "O": 2},
        "G": {"C": 2, "H": 3, "N": 1, "O": 1},
        "H": {"C": 6, "H": 7, "N": 3, "O": 1},
        "I": {"C": 6, "H": 11, "N": 1, "O": 1},
        "L": {"C": 6, "H": 11, "N": 1, "O": 1},
        "K": {"C": 6, "H": 12, "N": 2, "O": 1},
        "M": {"C": 5, "H": 9, "N": 1, "O": 1, "S": 1},
        "F": {"C": 9, "H": 9, "N": 1, "O": 1},
        "P": {"C": 5, "H": 7, "N": 1, "O": 1},
        "S": {"C": 3, "H": 5, "N": 1, "O": 2},
        "T": {"C": 4, "H": 7, "N": 1, "O": 2},
        "W": {"C": 11, "H": 10, "N": 2, "O": 1},
        "Y": {"C": 9, "H": 9, "N": 1, "O": 2},
        "V": {"C": 5, "H": 9, "N": 1, "O": 1},
    }

    def __init__(
        self,
        aa_seq: str | None = None,
        strict: bool = False
    ):
        if not isinstance(strict, bool):
            raise TypeError(
                "Polypeptide argument 'strict' must be bool, got "
                + type(strict).__name__
            )

        self._strict = strict
        self.aa_seq = aa_seq if aa_seq is not None else ""

    @property
    def strict(self) -> bool:
        """Getter for strict mode."""
        return self._strict

    @property
    def aa_seq(self) -> str:
        """Getter for the amino acid sequence."""
        return self._aa_seq

    @aa_seq.setter
    def aa_seq(self, aa_seq: str) -> None:
        """Setter for the amino acid sequence."""
        if aa_seq is None:
            aa_seq = ""
        if not isinstance(aa_seq, str):
            raise TypeError(
                "Polypeptide argument 'aa_seq' must be str, not "
                + type(aa_seq).__name__
            )

        aa_seq = aa_seq.upper()

        if self._strict:
            if invalid := set(aa_seq) - self.VALID_AA:
                raise ValueError(
                    f"(Strict Mode) Invalid amino acid(s) found: {invalid}"
                )

        self._aa_seq = aa_seq

    def copy(self, strict: bool | None = None) -> "Polypeptide":
        """Returns a copy of the Polypeptide instance."""
        new_strict = strict if strict is not None else self._strict
        return Polypeptide(self.aa_seq, strict=new_strict)

    def to_strict(self) -> "Polypeptide":
        """Returns a strict copy of the Polypeptide instance."""
        return self.copy(strict=True)

    def mass(self, accuracy: int = 3) -> float:
        """Calculates the molecular mass of the polypeptide."""
        if not self.aa_seq:
            return 0.0
        total = sum(self.AA_MASS.get(aa, 0) for aa in self.aa_seq) + 18.01528
        return round(total, accuracy)

    def composition(self) -> dict:
        """Returns the amino acid composition as a dictionary."""
        return dict(Counter(self.aa_seq))

    def count(self, aa: str) -> int:
        """Returns the count of a specific amino acid in the sequence."""
        return self.aa_seq.count(aa)

    def subseq(self, start: int, end: int | None = None) -> "Polypeptide":
        """Returns a subsequence from start to end (exclusive)."""
        sub = self.aa_seq[start:end]

        return Polypeptide(sub, strict=self._strict)

    def formula(self) -> str:
        """Calculates the molecular formula of the polypeptide."""
        if not self.aa_seq:
            return ""

        atom_count: defaultdict[str, int] = defaultdict(int)

        for aa in self.aa_seq:
            if aa not in self.RESIDUE_FORMULA:
                raise ValueError(
                    f"Unknown amino acid '{aa}' in sequence. "
                    "Molecular formula can only be computed for "
                    "standard amino acids."
                )

            for atom, num in self.RESIDUE_FORMULA[aa].items():
                atom_count[atom] += num

        atom_count["H"] += 2
        atom_count["O"] += 1

        order = ["C", "H"] + sorted(set(atom_count.keys()) - {"C", "H"})

        formula = []
        for element in order:
            count = atom_count[element]
            if count > 0:
                formula.append(element + (str(count) if count > 1 else ""))

        return " ".join(formula)

    def is_valid(self) -> bool:
        """Checks if the polypeptide sequence is valid."""
        return not (set(self.aa_seq) - self.VALID_AA)

    def __len__(self) -> int:
        return len(self.aa_seq)

    def __str__(self) -> str:
        return self.aa_seq

    def __repr__(self) -> str:
        from omibio.utils.truncate_repr import truncate_repr
        aa_seq_repr = truncate_repr(self.aa_seq)
        return f"Polypeptide({aa_seq_repr}, strict={self.strict})"

    def __getitem__(self, idx) -> str:
        return self.aa_seq[idx]

    def __setitem__(self, idx: int, new_aa: str) -> None:
        aa_seq_list = list(self.aa_seq)
        aa_seq_list[idx] = new_aa
        self.aa_seq = "".join(aa_seq_list)

    def __iter__(self):
        return iter(self.aa_seq)

    def __contains__(self, item) -> bool:
        return item in self.aa_seq

    def __eq__(self, other) -> bool:
        if isinstance(other, Polypeptide):
            return self.aa_seq == other.aa_seq
        elif isinstance(other, str):
            return self.aa_seq == other.upper()

        return False

    def __add__(self, other) -> "Polypeptide":
        if isinstance(other, Polypeptide):
            strict_mode = self._strict or other.strict
            return Polypeptide(self.aa_seq + other.aa_seq, strict=strict_mode)

        elif isinstance(other, str):
            other = other.upper()
            return Polypeptide(
                self.aa_seq + other, strict=self._strict
            )

        else:
            raise TypeError(
                "Can only add Polypeptide or str to Polypeptide, got "
                + type(other).__name__
            )

    def __mul__(self, n: int) -> "Polypeptide":
        if not isinstance(n, int):
            raise TypeError(
                "Polypeptide Can only multiply by int, got "
                + type(n).__name__
            )
        if n < 0:
            raise ValueError(
                "Polypeptide cannot be multiply by a negative number"
            )

        return Polypeptide(
            self.aa_seq * n, strict=self._strict
        )


def main():
    poly1 = Polypeptide('ADQLLKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWS')
    poly1[1: 5] = "LLLL"
    print(repr(poly1))


if __name__ == "__main__":
    main()
