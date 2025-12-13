from io import (
    DEFAULT_BUFFER_SIZE,
    SEEK_CUR,
    SEEK_END,
    SEEK_SET,
    BufferedReader,
    RawIOBase,
)
from sys import maxsize
from typing import (
    TYPE_CHECKING,
    Any,
)


if TYPE_CHECKING:
    from .lz4 import LZ4Decompressor
    from .zstd import ZSTDDecompressor


class DecompressReader(RawIOBase):
    """Adapts the decompressor API to a RawIOBase reader API."""

    def __init__(
        self,
        fp: BufferedReader,
        decomp_factory: object,
        trailing_error: tuple = (),
        **decomp_args: dict[str, Any],
    ) -> None:

        self._fp = fp
        self._eof = False
        self._pos = 0
        self._size = -1
        self._decomp_factory = decomp_factory
        self._decomp_args = decomp_args
        self._decompressor: LZ4Decompressor | ZSTDDecompressor = (
            self._decomp_factory(**self._decomp_args)
        )
        self._trailing_error = trailing_error

    def close(self) -> None:

        self._decompressor = None
        return super().close()

    def readable(self) -> bool:

        return True

    def seekable(self) -> bool:

        return self._fp.seekable()

    def readinto(self, b: bytes | bytearray) -> int:

        with memoryview(b) as view, view.cast("B") as byte_view:
            data = self.read(len(byte_view))
            byte_view[:len(data)] = data
        return len(data)

    def read(self, size: int = -1) -> bytes:

        if size < 0:
            return self.readall()

        if not size or self._eof:
            return b""

        data = None

        while True:
            if self._decompressor.eof:
                rawblock = (
                    self._decompressor.unused_data or
                    self._fp.read(DEFAULT_BUFFER_SIZE)
                )

                if not rawblock:
                    break

                self._decompressor = self._decomp_factory(
                    **self._decomp_args,
                )

                try:
                    data = self._decompressor.decompress(rawblock, size)
                except self._trailing_error:
                    break

            else:
                if self._decompressor.needs_input:
                    rawblock = self._fp.read(DEFAULT_BUFFER_SIZE)
                    if not rawblock:
                        raise EOFError(
                            "Compressed file ended before the "
                            "end-of-stream marker was reached",
                        )
                else:
                    rawblock = b""
                data = self._decompressor.decompress(rawblock, size)

            if data:
                break

        if not data:
            self._eof = True
            self._size = self._pos
            return b""

        self._pos += len(data)
        return data

    def readall(self) -> bytes:

        chunks = []

        while data := self.read(maxsize):
            chunks.append(data)

        return b"".join(chunks)

    def _rewind(self) -> None:

        self._fp.seek(0)
        self._eof = False
        self._pos = 0
        self._decompressor = self._decomp_factory(**self._decomp_args)

    def seek(self, offset: int, whence: int = SEEK_SET) -> int:

        if whence == SEEK_SET:
            """Do nothing."""
        elif whence == SEEK_CUR:
            offset = self._pos + offset
        elif whence == SEEK_END:
            if self._size < 0:

                while self.read(DEFAULT_BUFFER_SIZE):
                    """Do nothing."""

            offset = self._size + offset
        else:
            raise ValueError("Invalid value for whence: {}".format(whence))

        if offset < self._pos:
            self._rewind()
        else:
            offset -= self._pos

        while offset > 0:
            data = self.read(min(DEFAULT_BUFFER_SIZE, offset))
            if not data:
                break
            offset -= len(data)

        return self._pos

    def tell(self) -> int:

        return self._pos
