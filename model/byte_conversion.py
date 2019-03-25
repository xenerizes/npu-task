from struct import pack
from .defines import *

_options = {
    1: '>b',
    2: '>h',
    4: '>i',
    8: '>q'
}

_bytes_in = {
    127: 1,
    32767: 2,
    2147483647: 4
}


def portmask_bits(portmask):
    if portmask is None:
        return '0' * 8
    return '{0:08b}'.format(portmask)[::-1]


def to_bytes(intval, bytenum):
    try:
        bytestr = pack(_options[bytenum], intval)
        return [b for b in bytestr]
    except Exception:
        raise Exception("Bad params for conversion of \"{}\" in {} byte(s)"
                        .format(intval, bytenum))


def guess_byte_count(intval):
    for val, bytes in _bytes_in.items():
        if intval < val:
            return bytes
    return 8


def to_register(intval):
    bytelen = guess_byte_count(intval)
    bytestr = pack(_options[bytelen], intval)
    bytelist = [b for b in bytestr]
    while len(bytelist) > 0 and bytelist[0] is 0:
        bytelist.pop(0)
    return bytelist + [0] * (REGISTER_LEN - len(bytelist))


def mem_to_str_be(intarray):
    return "0x" + " 0x".join("{:02x}".format(c) for c in intarray)


def mem_to_str_le(intarray):
    return "0x" + " 0x".join("{:02x}".format(c) for c in reversed(intarray))


def bytestr(intarray):
    return bytes(bytearray(intarray))
