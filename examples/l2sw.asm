.parser
    store PHV, HEADER, 12
    mov r1, PHV+6, 6
    cmpje r1, 0xffffffffffff, halt

.match_action 1
    mov r1, PHV+6, 6
    call exact_match
    cmpje r1, 1, done
    ctrl
done:

.match_action 2
    load r1, PHV+12, 6
    call exact_match
    cmpje r2, 1, not_found
    ori PORTMASK, r1
    j done
not_found:
    mov PORTMASK, -1
done:

.deparser
