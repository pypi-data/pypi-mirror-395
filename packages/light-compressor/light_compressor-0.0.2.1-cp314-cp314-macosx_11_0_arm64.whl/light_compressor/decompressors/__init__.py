"""Simple stream readers for compressed buffers."""

from .decompress_reader import DecompressReader
from .lz4 import LZ4Decompressor
from .zstd import ZSTDDecompressor


__all__ = (
    "DecompressReader",
    "LZ4Decompressor",
    "ZSTDDecompressor",
)
