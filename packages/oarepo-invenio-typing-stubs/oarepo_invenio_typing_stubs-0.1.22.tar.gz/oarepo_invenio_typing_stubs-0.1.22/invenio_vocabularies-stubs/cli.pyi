from typing import Any

from flask.cli import with_appcontext
from invenio_vocabularies.datastreams import DataStreamFactory as DataStreamFactory
from invenio_vocabularies.factories import (
    get_vocabulary_config as get_vocabulary_config,
)

def vocabularies() -> None: ...
def _process_vocab(
    config: dict[str, Any],
    num_samples: int | None = ...,
) -> tuple[int, int, int]: ...
def _output_process(
    vocabulary: str,
    op: str,
    success: int,
    errored: int,
    filtered: int,
) -> None: ...
@with_appcontext
def import_vocab(
    vocabulary: str,
    filepath: str | None = ...,
    origin: str | None = ...,
    num_samples: int | None = ...,
) -> None: ...
@with_appcontext
def update(
    vocabulary: str,
    filepath: str | None = ...,
    origin: str | None = ...,
) -> None: ...
@with_appcontext
def convert(
    vocabulary: str,
    filepath: str | None = ...,
    origin: str | None = ...,
    target: str | None = ...,
    num_samples: int | None = ...,
) -> None: ...
@with_appcontext
def delete(
    vocabulary: str,
    identifier: str | None,
    all: bool,
) -> None: ...
