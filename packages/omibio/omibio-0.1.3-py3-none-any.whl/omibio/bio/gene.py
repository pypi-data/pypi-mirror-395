from omibio.sequence.sequence import Sequence

# TODO: Needs modification


class Gene(Sequence):
    """
    A subclass of Sequence representing a gene with biological metadata.
    """

    def __init__(self, sequence: str, name: str, organism: str):
        """Initialize Gene with sequence, name, and organism."""
        super().__init__(sequence)  # Initialize base class
        self.name = name
        self.organism = organism

    def __repr__(self) -> str:
        return (f"Gene('{self.name}' from '{self.organism}')")

    def get_info(self) -> str:
        """
        Return formatted information about the gene.
        """
        gc_content = super().gc_content(True)  # Get GC content from base class
        return (
            f"Gene {self.name} from {self.organism}, "
            f"Length: {len(self)} bp, GC content: {gc_content}"
        )

    def mutate(self, position: int, new_base: str) -> None:
        """
        Perform a point mutation at a specific position (1-based index).

        Args:
            position: The index of the base to mutate.
            new_base: The new nucleotide (A, T, C, or G).

        Raises:
            IndexError: If the position is out of range.
            ValueError: If the new base is invalid.
        """
        idx = position - 1  # Convert to 0-based index
        # Check position validity
        if not (0 <= idx < len(self)):
            raise IndexError("Position out of range")

        seq_list = list(self.sequence)
        seq_list[idx] = new_base  # Perform mutation
        self.sequence = "".join(seq_list)  # Update sequence


def main():
    gene = Gene("ACGTAGTCAGTCAGTC", "Name", "Organism")
    print(gene.get_info())


if __name__ == "__main__":
    main()
