from .pipeline import *


def run(commands, tables, packets):
    parse = Parser(commands.parser)
    ma = MatchAction(commands.matchaction, tables[0])
    deparse = Deparser(commands.deparser)

    output_packets = []

    for packet in packets:
        context = parse.process(packet)
        context = ma.process(packet, context)
        output_packets.append(deparse.process(packet, context))

    return output_packets
