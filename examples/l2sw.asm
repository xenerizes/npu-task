.parser
    store PHV, HEADER, 12
    mov r1, PHV, 6
    cmpje r1, 0xffffffffffff, halt

.match_action 1
    mov r1, PHV+6, 6
    call exact_match
    cmpje r1, 1, done
    or PORTMASK, 0x80
done:

.match_action 2
    mov r1, PHV+6, 6
    call exact_match
    cmpje r2, 1, not_found
    or PORTMASK, r1
    j done
not_found:
    or PORTMASK, 0xff
done:

.deparser
