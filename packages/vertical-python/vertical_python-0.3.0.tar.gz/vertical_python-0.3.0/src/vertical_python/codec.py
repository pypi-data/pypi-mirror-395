"""
Import this module to register vertical python as a codec
"""

import codecs

from vertical_python import rotate, encode_py_to_vpy


def encoder(text: str) -> tuple[bytes, int]:
    return encode_py_to_vpy(text).encode("utf-8"), len(text)


def decoder(text: bytes | memoryview) -> tuple[str, int]:
    rotated = rotate(text)
    return rotated, len(text)


def vertical_codec(encoding_name: str):
    return codecs.CodecInfo(encoder, decoder, name="vertical")

codecs.register(vertical_codec)
