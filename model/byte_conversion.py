from struct import pack

_options = {
    1: '>b',
    2: '>h',
    4: '>i',
    8: '>q'
}


def to_bytes(intval, bytenum):
    try:
        return pack(_options[bytenum], intval)
    except Exception:
        raise Exception("Bad params for conversion of \"{}\" in {} byte(s)"
                        .format(intval, bytenum))
