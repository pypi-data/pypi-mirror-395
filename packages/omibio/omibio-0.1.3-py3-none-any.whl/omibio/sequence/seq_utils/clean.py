from omibio.sequence.sequence import Sequence, Polypeptide
from typing import Literal, Iterable, Mapping
import re
from dataclasses import dataclass


@dataclass
class CleanReportItem:
    orig_name: str
    clean_name: str | None = None
    orig_len: int = 0
    clean_len: int = 0
    removed: bool = False
    gap_policy: str | None = None
    illegal_removed: int = 0
    illegal_replaced: int = 0
    name_changed: bool = False
    reason: str = ""


class CleanReport:

    def __init__(self):
        self._records: list[CleanReportItem] = []

    def add(self, item: CleanReportItem):
        if not isinstance(item, CleanReportItem):
            raise TypeError(
                "add() argument 'item' must be CleanReportItem, got "
                + type(item).__name__
            )
        self._records.append(item)

    @property
    def records(self) -> list[CleanReportItem]:
        return self._records

    @property
    def kept(self):
        return [r for r in self._records if not r.removed]

    @property
    def removed(self):
        return [r for r in self._records if r.removed]

    def summary(self):
        return {
            "total": len(self._records),
            "kept": len(self.kept),
            "removed": len(self.removed)
        }


VALID_BASES = {
    "A", "T", "C", "G", "U",
    "N", "R", "Y", "K", "M", "B", "V", "D", "H", "S", "W"
}
WHITESPACE_RE = re.compile(r"\s+")
INVALID_NAME_CHAR_RE = re.compile(r"[^ A-Za-z0-9_.-]")
ALIG_SYMBOL_RE = re.compile(r"-+")


def clean(
    seqs: Mapping[str, str | Sequence | Polypeptide],
    name_policy: Literal["keep", "id_only", "underscores"] = "keep",
    gap_policy: Literal["keep", "remove", "collapse"] = "keep",
    strict: bool = False,
    min_len: int = 10,
    max_len: int = 100_000,
    normalize_case: bool = True,
    remove_illegal: bool = False,
    allowed_bases: Iterable[str] | None = None,
    remove_empty: bool = True,
    as_str: bool = True,
    as_polypeptide: bool = False,
    report: bool = False
) -> (
    dict[str, str | Sequence | Polypeptide]
    | tuple[dict[str, str | Sequence | Polypeptide], CleanReport]
):
    """Clean sequences according to specified policies.

    Args:
        seqs (dict[str, str  |  Sequence]):
            Dictionary of sequence names to sequences
            (as strings or Sequence objects).
        name_policy (Literal["keep", "id_onbly", "underscores"], optional):
            Policy for cleaning sequence names. Defaults to "keep".
        gap_policy (Literal["keep", "remove", "collapse"], optional):
            Policy for handling gaps in sequences. Defaults to "keep".
        strict (bool, optional):
            If True, raises an error on illegal characters. Defaults to False.
        min_len (int, optional):
            Minimum length for sequences to keep. Defaults to 10.
        max_len (int, optional):
            Maximum length for sequences to keep. Defaults to 100,000.
        normalize_case (bool, optional):
            If True, converts sequences to uppercase. Defaults to True.
        remove_illegal (bool, optional):
            If True, removes illegal characters instead of replacing
            them with 'N'. Defaults to False.
        allowed_bases (set[str] | None, optional):
            Set of allowed bases. Defaults to VALID_BASES.
        remove_empty (bool, optional):
            If True, removes sequences that are empty or contain only 'N's.
            Defaults to True.
        as_str (bool, optional):
            If True, returns cleaned sequences as strings.
            If False, returns them as Sequence objects. Defaults to True.
        report (bool, optional):
            If True, generates a cleaning report. Defaults to False.

    Raises:
        ValueError:
            If input values are invalid.
        TypeError:
            If input types are incorrect.

    Returns:
        dict[str, str | Sequence] |
        tuple[dict[str, str | Sequence], CleanReport]:
            Cleaned sequences, optionally with a cleaning report.
    """

    if allowed_bases is None:
        allowed_bases = VALID_BASES
    else:
        allowed_bases = set(allowed_bases)
    for base in allowed_bases:
        if not isinstance(base, str) or len(base) != 1:
            raise ValueError(
                "clean() argument 'allowed_bases' must be an iterable "
                "of single-character strings."
            )
    if not isinstance(seqs, dict):
        raise TypeError(
            f"clean() argument 'seqs' must be dict, got {type(seqs).__name__}"
        )
    if name_policy not in {"keep", "id_only", "underscores"}:
        raise ValueError(
            "clean() argument 'name_policy' must be one of: "
            "'keep', 'id_only', 'underscores'"
        )
    if gap_policy not in {"keep", "remove", "collapse"}:
        raise ValueError(
            "clean() argument 'gap_policy' must be one of: "
            "'keep', 'remove', 'collapse'"
        )
    if not isinstance(min_len, int):
        raise TypeError(
            "clean() argument 'min_len' must be int, got "
            + type(min_len).__name__
        )
    if not isinstance(max_len, int):
        raise TypeError(
            "clean() argument 'max_len' must be int, got "
            + type(max_len).__name__
        )
    if min_len < 0 or max_len < 0:
        raise ValueError(
            "clean() argument 'min_len' and 'max_len' must be "
            "non-negative numbers"
        )
    if min_len > max_len:
        raise ValueError(
            "clean() argument 'min_len' cannot be larger than 'max_len'"
        )
    cleaned_seqs = {}
    if report:
        clean_report = CleanReport()

    # ---------------- name processing ----------------
    def process_name(name) -> str:
        name = WHITESPACE_RE.sub(" ", name.strip())

        if name_policy == "id_only":
            name = name.split(" ", 1)[0]

        name = INVALID_NAME_CHAR_RE.sub("_", name)

        if name_policy == "underscores":
            name = name.replace(" ", "_")

        if not name:
            name = "unnamed"

        return name

    # ---------------- sequence cleaning ----------------
    def process_seq(seq: str, item: CleanReportItem) -> str:

        pure_seq = WHITESPACE_RE.sub("", seq)
        item.orig_len = len(pure_seq)

        cleaned = pure_seq
        if normalize_case:
            cleaned = cleaned.upper()

        match gap_policy:
            case "remove":
                item.gap_policy = "remove"
                cleaned = cleaned.replace("-", "")
            case "collapse":
                item.gap_policy = "collapse"
                cleaned = ALIG_SYMBOL_RE.sub("-", cleaned)
            case _:
                item.gap_policy = "keep"

        if strict:
            for i, base in enumerate(cleaned):
                if base not in allowed_bases and base != "-":
                    raise ValueError(
                        f"Illegal character {base} in sequence at position {i}"
                    )
        else:
            illegal_removed = 0
            illegal_replaced = 0
            new_seq = []

            for base in cleaned:
                if base in allowed_bases or base == "-":
                    new_seq.append(base)
                else:
                    if remove_illegal:
                        illegal_removed += 1
                    else:
                        new_seq.append("N")
                        illegal_replaced += 1

            cleaned = "".join(new_seq)
            item.illegal_removed = illegal_removed
            item.illegal_replaced = illegal_replaced

        if remove_empty and set(cleaned) <= {"N", "-"}:
            item.reason = "empty_or_N_only"
            return ""

        if not cleaned or not (min_len <= len(cleaned) <= max_len):
            item.reason = "length_filter"
            return ""

        return cleaned

    # ---------------- main loop ----------------
    for raw_name, raw_seq in seqs.items():
        if not isinstance(raw_name, str):
            raise TypeError(
                "Sequence name must be a string, got "
                + type(raw_name).__name__
            )
        if not isinstance(raw_seq, (str, Sequence)):
            raise TypeError(
                f"Sequence '{raw_name}' must be a string or Sequence, "
                f"got {type(raw_seq).__name__}"
            )

        item = CleanReportItem(orig_name=raw_name)

        cleaned_name = process_name(raw_name)

        cleaned = process_seq(str(raw_seq), item)

        if not cleaned:
            item.removed = True
            item.clean_len = 0
            if report:
                clean_report.add(item)
            continue

        if cleaned_name in cleaned_seqs:
            count = 1
            new_name = f"{cleaned_name}_{count}"
            while new_name in cleaned_seqs:
                count += 1
                new_name = f"{cleaned_name}_{count}"
            cleaned_name = new_name

        item.clean_name = cleaned_name
        item.clean_len = len(cleaned)

        if cleaned_name != raw_name:
            item.name_changed = True

        cleaned_seq: str | Sequence | Polypeptide
        if not as_str:
            if as_polypeptide:
                cleaned_seq = Polypeptide(cleaned)
            else:
                cleaned_seq = Sequence(cleaned)
        else:
            cleaned_seq = cleaned

        cleaned_seqs[cleaned_name] = cleaned_seq

        if report:
            clean_report.add(item)

    if not report:
        return cleaned_seqs
    else:
        return cleaned_seqs, clean_report


def write_report(out_path: str, report: CleanReport) -> None:
    """Write a cleaning report to a text file.

    Args:
        out_path (str): Path to the output report file.
        report (CleanReport): The cleaning report to write.
    Raises:
        TypeError:
            If input types are incorrect.
    """

    if not isinstance(out_path, str):
        raise TypeError(
            "write_report() argument 'out_path' must be str, got "
            + type(out_path).__name__
        )
    if not isinstance(report, CleanReport):
        raise TypeError(
            "write_report() argument 'report' must be CleanReport, got "
            + type(report).__name__
        )

    lines = []

    # --- Summary ---
    lines.append("=== Clean Report Summary ===")
    summary = report.summary()
    lines.append(f"Total sequences: {summary['total']}")
    lines.append(f"Kept: {summary['kept']}")
    lines.append(f"Removed: {summary['removed']}")
    lines.append("")

    # --- Kept sequences table ---
    lines.append("=== Cleaned Sequences ===")
    headers = [
        "orig_name", "clean_name",
        "orig_len", "clean_len",
        "name_changed", "gap_policy",
        "illegal_removed", "illegal_replaced"
    ]

    # Prepare rows
    rows = []
    for r in report.kept:
        rows.append([
            r.orig_name,
            r.clean_name,
            str(r.orig_len),
            str(r.clean_len),
            "yes" if r.name_changed else "no",
            r.gap_policy if r.gap_policy else "",
            str(r.illegal_removed),
            str(r.illegal_replaced)
        ])

    # Column widths
    col_widths = [
        max(
            len(headers[i]), max((len(row[i]) for row in rows), default=0)
        ) for i in range(len(headers))
    ]

    # Header row
    header_line = "  ".join(
        headers[i].ljust(col_widths[i]) for i in range(len(headers))
    )
    lines.append(header_line)
    lines.append("-" * len(header_line))

    # Data rows
    for row in rows:
        lines.append(
            "  ".join(row[i].ljust(col_widths[i]) for i in range(len(headers)))
        )
    lines.append("")

    # --- Removed sequences ---
    lines.append("=== Removed Sequences ===")
    lines.append("orig_name          reason")
    lines.append("-" * 50)
    for r in report.removed:
        reason = getattr(r, "reason", "removed")
        lines.append(f"{r.orig_name.ljust(18)} {reason}")

    # Write to file
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    from omibio.io import write_fasta, read
    input_path = "./examples/data/example_dirty.fasta"
    output_path = "./examples/output/clean_fasta_output.fasta"
    report_path = "./examples/output/clean_report.txt"

    seqs = read_fasta(input_path, strict=False).seq_dict()

    cleaned_seqs, report = clean(
        seqs, name_policy="id_only", gap_policy="collapse",
        report=True, remove_illegal=True
    )

    write_fasta(output_path, cleaned_seqs, space_between=True)
    print(f"Cleaned: {output_path}")

    write_report(report_path, report)
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
