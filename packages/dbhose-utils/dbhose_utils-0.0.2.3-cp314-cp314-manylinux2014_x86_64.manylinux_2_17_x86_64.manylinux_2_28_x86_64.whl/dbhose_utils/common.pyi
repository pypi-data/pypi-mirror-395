"""Metadata convert functions."""

from collections.abc import Generator
from typing import Any

from nativelib import (
    Column,
    NativeReader,
)
from pgcopylib import (
    PGCopyReader,
    PGOid,
)
from pgpack import PGPackReader


def pgoid_from_metadata(metadata: bytes) -> list[PGOid]:
    """Convert PGPack metadata to PGCopy metadata."""

    ...


def columns_from_metadata(
    metadata: bytes,
    is_nullable: bool = True,
) -> list[Column]:
    """Convert PGPack metadata to Native column_list."""

    ...


def metadata_from_columns(column_list: list[Column]) -> bytes:
    """Convert Native column_list to PGPack metadata."""

    ...


def recover_rows(
    reader: NativeReader | PGCopyReader | PGPackReader,
) -> Generator[Any, None, None]:
    """Read rows from broken reader."""

    ...
