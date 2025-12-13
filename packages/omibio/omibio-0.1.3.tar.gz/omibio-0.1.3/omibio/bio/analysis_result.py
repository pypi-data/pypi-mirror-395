from omibio.bio.seq_interval import SeqInterval
from dataclasses import dataclass, field
from matplotlib.axes import Axes
from typing import Callable, Iterator, Any


@dataclass
class AnalysisResult:
    """Analysis result storing a list of SeqInterval objects."""

    intervals: list[SeqInterval]

    type: str | None = None
    seq_id: str | None = None
    plot_func: Callable | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.intervals, list):
            raise TypeError(
                "AnalysisResult argument 'intervals' must be list, got "
                + type(self.intervals).__name__
            )
        if (
            self.plot_func is not None
            and not isinstance(self.plot_func, Callable)
        ):
            raise TypeError(
                "AnalysisResult argument 'plot_func' must be Callable, got "
                + type(self.plot_func).__name__
            )
        if not isinstance(self.metadata, dict):
            raise TypeError(
                "AnalysisResult argument 'metadata' must be dict, got "
                + type(self.plot_func).__name__
            )

    def plot(self, **kwargs) -> Axes:
        if self.plot_func is None:
            raise NotImplementedError(
                "Plotting is not supported for this analysis."
            )

        return self.plot_func(self, **kwargs)

    def to_dict(self, prefix: str = "Analysis Result"):
        if not isinstance(prefix, str):
            raise TypeError(
                "to_dict argument 'prefix' must be dict, got "
                + type(self.plot_func).__name__
            )
        interval_dict = {}
        for i, interval in enumerate(self.intervals):
            if not interval.nt_seq:
                continue
            interval_dict[f"{prefix}_{i+1}"] = interval.nt_seq

        return interval_dict

    def __len__(self) -> int:
        return len(self.intervals)

    def __iter__(self) -> Iterator[SeqInterval]:
        return iter(self.intervals)

    def __getitem__(self, idx: int | slice) -> SeqInterval | list[SeqInterval]:
        return self.intervals[idx]

    def __repr__(self) -> str:
        return (
            f"AnalysisResult(intervals={self.intervals!r}, "
            f"seq_id={self.seq_id!r}, type={self.type!r})"
        )

    def __str__(self) -> str:
        return str(self.intervals)


def main():
    from omibio.io import read_fasta
    from omibio.analysis import find_orfs

    res = find_orfs(
        read_fasta("./examples/data/example_single_long_seq.fasta")["example"]
    )
    print(res.to_dict())


if __name__ == "__main__":
    main()
