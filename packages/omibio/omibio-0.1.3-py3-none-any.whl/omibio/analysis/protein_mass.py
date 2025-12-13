from omibio.sequence.polypeptide import Polypeptide


def calc_mass(aa_seq: Polypeptide | str, accuracy: int = 3) -> float:
    """Calculate the molecular weight of a polypeptide chain molecule.

    Args:
        aa_seq (Polypeptide | str):
            A polypeptide sequence as a Polypeptide object
            or a string of amino acid single-letter codes.
        accuracy (int, optional):
            The number of decimal places to round the mass to. Defaults to 3.

    Raises:
        TypeError: If aa_seq is not a Polypeptide or str.

    Returns:
        float: The molecular weight of the polypeptide chain.
    """
    if not isinstance(aa_seq, (Polypeptide, str)):
        raise TypeError(
            "calc_mass() argument 'aa_seq' must be Polypeptide or str, got "
            + type(aa_seq).__name__
        )
    if isinstance(aa_seq, str):
        aa_seq = Polypeptide(aa_seq)

    return aa_seq.mass(accuracy)


def main():
    print(calc_mass("A"))


if __name__ == "__main__":
    main()
