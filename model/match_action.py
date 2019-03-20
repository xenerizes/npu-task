class MatchAction(object):
    def __init__(self, commands, table):
        self.commands = commands
        self.table = table
        self.phv = None
        self.portmask = None

    def process(self, packet, context):
        for cmd in self.commands:
            context = cmd.call(context, self.table)
        return packet, context