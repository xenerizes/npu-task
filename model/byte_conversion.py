from struct import pack
from .defines import *

max_int64 = 0xFFFFFFFFFFFFFFFF

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
    return '{0:08b}'.format(portmask)


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
    return 16


def pack_16(intval):
    return pack('>QQ', (intval >> 64) & max_int64, intval & max_int64)


def to_register(intval):
    bytelen = guess_byte_count(intval)
    if bytelen == 16:
        bytestr = pack_16(intval)
    else:
        bytestr = pack(_options[bytelen], intval)
    bytelist = [b for b in bytestr]
    while len(bytelist) > 0 and bytelist[0] is 0:
        bytelist.pop(0)
    return bytelist + [0] * (REGISTER_LEN - len(bytelist))


def to_intval(register):
    return int.from_bytes(register, 'little')


def mem_to_str_be(intarray):
    return "0x" + " 0x".join("{:02x}".format(c) for c in intarray)


def mem_to_str_le(intarray):
    return "0x" + " 0x".join("{:02x}".format(c) for c in reversed(intarray))


def bytestr(intarray):
    return bytes(bytearray(intarray))

