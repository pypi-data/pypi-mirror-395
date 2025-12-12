import re
import struct

# Z85CHARS is the base 85 symbol table
Z85CHARS = bytearray(
    b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"
)
# Z85MAP maps integers in [0,84] to the appropriate character in Z85CHARS
Z85MAP = dict([(c, idx) for idx, c in enumerate(Z85CHARS)])

_85s = [85**i for i in range(5)]
_epadding = [0, 3, 2, 1]
_dpadding = [0, 4, 3, 2, 1]


class Z85DecodeError(Exception):
    pass


def z85encode(rawbytes) -> bytes:
    """encode raw bytes into Z85b"""
    rawbytes = bytearray(rawbytes)
    padding = _epadding[len(rawbytes) % 4]
    rawbytes = bytearray(rawbytes + b"\x00" * padding)
    nvalues = (len(rawbytes) + padding) // 4

    values = struct.unpack("<%dI" % nvalues, rawbytes)
    encoded = bytearray()
    for v in values:
        for offset in _85s:
            encoded.append(Z85CHARS[(v // offset) % 85])

    if padding:
        encoded = encoded[:-padding]
    return bytes(encoded)


def z85decode(z85bytes) -> bytes:
    """decode Z85b bytes to raw bytes"""
    z85bytes = bytearray(re.sub(b"\\s+", b"", z85bytes))
    padding = _dpadding[len(z85bytes) % 5]
    nvalues = (len(z85bytes) + padding) // 5
    values = []
    for i in range(0, len(z85bytes), 5):
        value = 0
        for j, offset in enumerate(_85s):
            try:
                value += Z85MAP[z85bytes[i + j]] * offset
            except IndexError:
                break  # we have reached the end of our input
            except KeyError as e:
                raise Z85DecodeError("Invalid byte code {!r}".format(e.args[0]))
        values.append(value)
    decoded = struct.pack("<%dI" % nvalues, *values)
    if padding:
        decoded = decoded[:-padding]
    return decoded
