class Parser(object):
    def __init__(self, commands):
        self.commands = commands

    def process(self, packet):
        context = []
        for cmd in self.commands:
            context.append(cmd.run(packet))
        return packet, context


class MatchAction(object):
    def __init__(self, commands, table):
        self.commands = commands
        self.table = table

    def process(self, packet, context):
        for cmd in self.commands:
            context = cmd.call(context, self.table)
        return packet, context


class Deparser(object):
    def __init__(self, commands):
        self.commands = commands

    def process(self, packet, context):
        for cmd in self.commands:
            packet = cmd.run(packet, context)
        return packet


