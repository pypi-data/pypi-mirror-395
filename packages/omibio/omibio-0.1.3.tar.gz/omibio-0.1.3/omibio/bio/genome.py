from omibio.bio.gene import Gene
from omibio.io.read_fasta import read_fasta

# TODO: Needs modifications


class Genome(object):
    """
    A class representing a genome, which is a collection of genes.
    """

    def __init__(self, organism: str):
        self.organism = organism  # organism name
        self._genes: list[Gene] = []  # internal list to store Gene objects
        self._gene_names: set[str] = set()  # to track existing gene names

    @property
    def genes(self) -> list[Gene]:
        """Return a list of Gene objects in the genome.

        Avoid direct modification by returning a copy.
        """
        return list(self._genes)

    def add_gene(self, gene: Gene) -> None:
        """Add a Gene object to the genome.

        Args:
            gene: Gene object to add.
        Raises:
            TypeError:
            If the provided object is not a Gene.
            ValueError:
            If the gene's organism does not match the genome's
            organism or if a gene with the same name already exists.
        """
        # check type
        if not isinstance(gene, Gene):
            raise TypeError(
                "add_gene() argument 'gene' must be Gene, not "
                + type(gene).__name__
            )
        # check organism match and unique name
        if gene.organism != self.organism:
            raise ValueError(
                f"Gene organism '{gene.organism}' does not match "
                f"genome organism '{self.organism}'."
            )
        # check unique name
        if gene.name in self._gene_names:
            raise ValueError(f"Gene name '{gene.name}' already exists")

        self._genes.append(gene)
        self._gene_names.add(gene.name)  # track the name

    def remove_gene(self, target: str | Gene) -> None:
        """Remove a Gene from the genome by name or by Gene object.

        Args:
            target: Gene object or gene name string to remove.
        Raises:
            TypeError:
            If the target is neither a Gene nor a string.
            ValueError:
            If the gene to remove does not exist in the genome.
        """
        # target is gene name
        if isinstance(target, str):
            name = target
            to_remove = None  # Gene to remove
            # Find the gene by name
            for gene in self._genes:
                if gene.name == name:
                    to_remove = gene
                    break
            # Not found
            if to_remove is None:
                raise ValueError(f"Gene '{name}' doesn't exist")
        # target is Gene object
        elif isinstance(target, Gene):
            to_remove = target
            # Check existence
            if to_remove not in self._genes:
                raise ValueError(f"Gene '{target.name}' doesn't exist")
        # Invalid type
        else:
            raise TypeError(
                "remove_gene() argument 'target' must be Gene or str, not "
                + type(target).__name__
            )

        self._genes.remove(to_remove)  # remove the gene
        self._gene_names.remove(to_remove.name)  # update name tracking

    def get(self, name: str) -> Gene:
        """Retrieve a Gene by its name.

        Args:
            name: Name of the gene to retrieve.
        Returns:
            Gene object with the specified name.
        Raises:
            ValueError:
            If no gene with the specified name exists in the genome.
        """
        for gene in self._genes:
            # Find gene by name
            if gene.name == name:
                return gene
        raise ValueError(f"Gene '{name}' not found")  # Not found

    def __len__(self) -> int:
        """Return the number of genes in the genome."""
        return len(self._genes)

    def average_gc_content(self, percent: bool = False) -> float | str | None:
        """Calculate the average GC content across all genes in the genome.

        Args:
            percent: If True, return GC content as a percentage string.
        Returns:
            Average GC content as a float or percentage string.
            Returns None if there are no genes in the genome.
        """
        # Handle empty genome
        if not self._genes:
            return None

        total_gc = 0.0
        for gene in self._genes:
            total_gc += float(gene.gc_content())  # sum GC content
        average_gc = total_gc / len(self._genes)  # calculate average

        # Return as float or percentage string
        return (
            average_gc if not percent
            else f"{(average_gc * 100):.2f}%"
            )

    def longest_gene(self) -> Gene | None:
        """Return the longest gene object in the genome."""
        if not self._genes:
            return None
        return max(self._genes, key=len)

    def to_fasta(self, file_name: str | None = None) -> str:
        """Return the genome in FASTA format.

        Args:
            file_name: Optional file name to write the FASTA output to.
        Returns:
            FASTA formatted string of the genome.
        Raises:
            OSError:
            If there is an error writing to the specified file.
        """
        fasta_lines = []
        for gene in self._genes:
            fasta_lines.append(f">{gene.name} [{gene.organism}]")
            fasta_lines.append(gene.sequence)

        # Write to file if specified
        if file_name:
            try:
                with open(file_name, "w") as f:
                    for line in fasta_lines:
                        f.write(f"{line}\n")
            except OSError as e:
                raise OSError(f"Failed to write to '{file_name}': {e}")

        return "\n".join(fasta_lines)  # Return FASTA string

    def read_fasta(self, file_name):
        """Read genes from a FASTA file and add them to the genome."""
        gene_dict = read_fasta(file_name, as_str=True)
        for name in gene_dict.keys():
            self.add_gene(Gene(gene_dict[name], name, self.organism))

    def to_dict(self) -> dict:
        """Return a dictionary representation of the genome.

        Keys are gene names and values are gene sequences."""
        gene_dict = {}
        for gene in self._genes:
            # Add gene name and sequence to dictionary
            gene_dict[gene.name] = gene.sequence
        return gene_dict

    def __str__(self) -> str:
        """Return a string representation of the genome."""
        return (
            f"Genome of {self.organism}" + str(self.genes)
        )


def main():
    gene1 = Gene("CCCCAGCGAGGCAGCTACTA", "Name1", "Organism")
    gene2 = Gene("ACGTAGCTACGTACGTAGCT", "Name2", "Organism")
    gene3 = Gene("ACAGTCGTACGTACGTACTA", "Name3", "Organism")
    genome = Genome("Organism")
    genome.add_gene(gene1)
    genome.add_gene(gene2)
    genome.add_gene(gene3)
    print(genome)
    print(f"Length: {len(genome)}")
    print(f"Longest: {genome.longest_gene()}")
    print(genome.get("Name1"))


if __name__ == "__main__":
    main()
