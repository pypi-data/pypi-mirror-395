from omibio.bio.seq_entry import SeqEntry
from omibio.sequence import Sequence, Polypeptide
from typing import Iterable


class SeqCollections:

    def __init__(
        self,
        entries: Iterable[SeqEntry] | None = None,
        source: str | None = None
    ):
        self._entries: dict[str, SeqEntry] = {}
        self._source = source
        if entries is not None and not isinstance(entries, Iterable):
            raise TypeError(
                "SeqCollections argument 'entries' must be Iterable "
                f"contains SeqEntry, got {type(entries).__name__}"
            )
        if entries:
            for entry in entries:
                self.add_entry(entry)

    @property
    def entries(self):
        return self._entries

    @property
    def source(self):
        return self._source

    def add_entry(self, entry: SeqEntry):
        if not isinstance(entry, SeqEntry):
            raise TypeError(
                "SeqCollections argument 'entries' must be Iterable "
                f"contains SeqEntry, got {type(entry).__name__}"
            )
        seq_id = entry.seq_id
        if seq_id in self._entries:
            raise ValueError(
                f"Duplicate seq_id '{seq_id}'"
            )
        if self._source != entry.source:
            raise ValueError(
                f"unmatch sources: {self._source} and {entry.source}"
            )
        self._entries[seq_id] = entry

    def get_entry(self, seq_id: str) -> SeqEntry:
        return self._entries[seq_id]

    def get_seq(self, seq_id: str) -> Sequence | Polypeptide:
        return self[seq_id]

    def seq_ids(self):
        return list(self._entries.keys())

    def seqs(self):
        return [e.seq for e in self._entries.values()]

    def entry_list(self):
        return list(self._entries.values())

    def seq_dict(self) -> dict[str, Sequence | Polypeptide]:
        return {e.seq_id: e.seq for e in self._entries.values()}

    def __iter__(self):
        return iter(self._entries.values())

    def __getitem__(self, seq_id: str) -> Sequence | Polypeptide:
        return self._entries[seq_id].seq

    def __contains__(self, seq_id: str) -> bool:
        return seq_id in self._entries

    def __len__(self):
        return len(self._entries)

    def __repr__(self):
        return f"SeqCollections({list(self._entries.values())!r})"

    def __str__(self):
        return str(list(self._entries.values()))


def main():
    seqs = SeqCollections(
        [
            SeqEntry(Sequence("ACTG"), seq_id="1"),
            SeqEntry(Sequence("ACTG"), seq_id="2"),
            SeqEntry(Sequence("ACTG"), seq_id="3"),
            SeqEntry(Sequence("ACTG"), seq_id="4"),
            SeqEntry(Sequence("ACTG"), seq_id="5"),
        ]
    )
    print(seqs)


if __name__ == "__main__":
    main()
