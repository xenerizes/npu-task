class Deparser(object):
    def __init__(self, commands):
        self.commands = commands
        self.phv = None
        self.header = None

    def process(self, packet, context):
        for cmd in self.commands:
            packet = cmd.run(packet, context)
        return packet
