class MatchAction(object):
    def __init__(self, data):
        self.text = data
        self.phv = None
        self.portmask = None

    def process(self, packet, header, portmask):
        return packet, header, portmask
