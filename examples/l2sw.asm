.parser
    store PHV, HEADER, 20
    mov r1, PHV+8, 6
    cmpje r1, 0xffffffffffff, halt

.match-action 1
    mov r1, PHV+8, 6
    call exact_match
    cmpje r1, 1, done
    ctrl
done:

.match-action 2
    mov r1, PHV+14, 6
    call exact_match
    cmpje r2, 1, not_found
    ori PORTMASK, r1
    j done
not_found:
    mov PORTMASK, -1
done:

.deparser
    load HEADER, PHV, 20