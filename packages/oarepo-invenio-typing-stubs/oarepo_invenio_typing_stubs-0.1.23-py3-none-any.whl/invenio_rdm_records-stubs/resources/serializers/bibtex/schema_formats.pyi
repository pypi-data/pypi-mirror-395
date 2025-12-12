class BibTexFormatter:
    """Formatter class for bibtex entry definitions."""

    book: dict[str, list[str] | str]
    booklet: dict[str, list[str] | str]
    misc: dict[str, list[str] | str]
    in_proceedings: dict[str, list[str] | str]
    proceedings: dict[str, list[str] | str]
    in_collection: dict[str, list[str] | str]
    in_book: dict[str, list[str] | str]
    article: dict[str, list[str] | str]
    unpublished: dict[str, list[str] | str]
    thesis: dict[str, list[str] | str]
    manual: dict[str, list[str] | str]
    dataset: dict[str, list[str] | str]
    software: dict[str, list[str] | str]
