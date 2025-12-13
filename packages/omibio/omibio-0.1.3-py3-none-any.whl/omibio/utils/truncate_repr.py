def truncate_repr(text: str | None, max_len: int = 30) -> str | None:
    """Truncate a string representation if it exceeds max_len.

    Args:
        text (str | None):
            The string to truncate.
        max_len (int, optional):
            Maximum length of the representation. Defaults to 30.

    Returns:
        str | None:
            Truncated representation of the string or None if text is None.
    """
    if not text:
        return None
    if len(text) <= max_len or max_len <= 3:
        return repr(text)
    half = (max_len - 3) // 2
    truncated = text[:half] + "..." + text[-half:]
    return repr(truncated)


def main():
    seq = "AGCTATGCTGATGCTAGTCTGATGCTGTAGTGCTAGTCTGTAGCACGATGCGAGTCACGATCTGATG"
    print(truncate_repr(seq))
    print(truncate_repr(None))


if __name__ == "__main__":
    main()
