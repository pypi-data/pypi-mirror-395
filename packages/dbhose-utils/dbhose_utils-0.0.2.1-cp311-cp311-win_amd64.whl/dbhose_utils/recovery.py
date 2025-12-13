from light_compressor import (
    auto_detector,
    define_writer,
)
from nativelib import (
    NativeReader,
    NativeWriter,
)
from pgcopylib import (
    PGCopyReader,
    PGCopyWriter,
    PGOid,
)
from pgpack import (
    PGPackReader,
    PGPackWriter,
)

from .common import recover_rows
from .detective import dump_detective


def dump_recovery(
    file_path: str,
    recovery_path: str | None = None,
) -> None:
    """Recover broken dump."""

    if not recovery_path:
        recovery_path = file_path + ".recovery"

    with open(file_path, "rb") as fileobj:
        compressor_method = auto_detector(fileobj)

    reader = dump_detective(file_path)

    if reader.__class__ is PGPackReader:
        recovery = PGPackWriter(
            open(recovery_path, "wb"),
            reader.metadata,
            reader.compression_method,
        )
        recovery.from_rows(recover_rows(reader))
        return recovery.close()

    if reader.__class__ is PGCopyReader:
        pgtypes = [
            PGOid.bytea
            for _ in range (reader.num_columns)
        ]
        recovery = PGCopyWriter(
            None,
            pgtypes,
        )
    elif reader.__class__ is NativeReader:
        reader.block_reader.read()
        column_list = reader.block_reader.column_list
        recovery = NativeWriter(column_list)
        reader = dump_detective(file_path)

    bytes_data = define_writer(
        bytes_data=recovery.from_rows(recover_rows(reader)),
        compressor_method=compressor_method,
    )

    with open(recovery_path, "wb") as fileobj:
        for data in bytes_data:
            fileobj.write(data)
