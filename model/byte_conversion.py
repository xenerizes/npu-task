from struct import pack

_options = {
    1: '>b',
    2: '>h',
    4: '>i',
    8: '>q'
}


def to_bytes(intval, bytenum):
    try:
        bytestr = pack(_options[bytenum], intval)
        return [b for b in bytestr]
    except Exception:
        raise Exception("Bad params for conversion of \"{}\" in {} byte(s)"
                        .format(intval, bytenum))


def to_register(intval):
    bytestr = pack('<qq', intval, 0)
    return [b for b in bytestr]


def bytestr(intarray):
    return bytes(bytearray(intarray))
