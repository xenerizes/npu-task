from scapy.all import *


def import_pcap():
    packets = rdpcap("port00_in.pcap")
    return packets


def export_pcap(packets):
    wrpcap("port00_out.pcap", packets)


if __name__ == "__main__":
    packets = import_pcap()
    export_pcap(packets)
