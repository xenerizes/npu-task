from struct import pack

CHAR_MAX = 127
SHORT_MAX = 37267
INT_MAX = 2147483647


def to_bytes(intval):
    if intval <= CHAR_MAX:
        return pack('>b', intval)
    if intval <= SHORT_MAX:
        return pack('>h', intval)
    if intval <= INT_MAX:
        return pack('>i', intval)
    else:
        return pack('>q', intval)
