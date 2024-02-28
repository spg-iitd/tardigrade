"""
Author:  Subrat Kumar Swain
Created:  21-02-2014
Description:  A PyTorch Dataset class for reading and parsing packets from a PCAP file.
"""
from torch.utils.data import IterableDataset
from scapy.utils import PcapReader

def get_traffic_vector(packet):
        """extracts the traffic vectors from packet

        Args:
            packet (scapy packet): input packet

        Returns:
            array: list of IPtype, srcMAC, dstMAC, srcIP, srcproto, dstIP, dstproto, time, packet size
        """
        packet = packet[0]

        # only process IP packets,
        if not (packet.haslayer(IP) or packet.haslayer(IPv6) or packet.haslayer(ARP)):
            return None

        timestamp = packet.time
        framelen = len(packet)
        if packet.haslayer(IP):  # IPv4
            srcIP = packet[IP].src
            dstIP = packet[IP].dst
            IPtype = 0
        elif packet.haslayer(IPv6):  # ipv6
            srcIP = packet[IPv6].src
            dstIP = packet[IPv6].dst
            IPtype = 1
        else:
            srcIP = ""
            dstIP = ""

        if packet.haslayer(TCP):
            srcproto = str(packet[TCP].sport)
            dstproto = str(packet[TCP].dport)
        elif packet.haslayer(UDP):
            srcproto = str(packet[UDP].sport)
            dstproto = str(packet[UDP].dport)
        else:
            srcproto = ""
            dstproto = ""

        if packet.haslayer(ARP):
            srcMAC = packet[ARP].hwsrc
            dstMAC = packet[ARP].hwdst
        else:
            srcMAC = packet.src
            dstMAC = packet.dst

        if srcproto == "":  # it's a L2/L1 level protocol
            if packet.haslayer(ARP):  # is ARP
                srcproto = "arp"
                dstproto = "arp"
                srcIP = packet[ARP].psrc  # src IP (ARP)
                dstIP = packet[ARP].pdst  # dst IP (ARP)
                IPtype = 0
            elif packet.haslayer(ICMP):  # is ICMP
                srcproto = "icmp"
                dstproto = "icmp"
                IPtype = 0
            elif srcIP + srcproto + dstIP + dstproto == "":  # some other protocol
                srcIP = packet.src  # src MAC
                dstIP = packet.dst  # dst MAC

        traffic_vector = [
            IPtype,
            srcMAC,
            dstMAC,
            srcIP,
            srcproto,
            dstIP,
            dstproto,
            float(timestamp),
            int(framelen),
        ]

        return traffic_vector


class PcapDataset(IterableDataset):
    """
    A PyTorch Dataset class for loading and processing packets from a PCAP file.

    This class iterates over packets in a PCAP file and extracts features from each packet.
    It supports applying optional transformations to the extracted features.

    Args:
        pcap_file (str): Path to the PCAP file.
        nb_samples (int): Maximum number of packets to process. If None, the entire dataset is processed.
        transform (callable, optional): A function/transform that takes in a packet tensor and returns a transformed tensor.
    """

    def __init__(self, pcap_file, nb_samples, transform=None):
        self.packets = PcapReader(pcap_file)
        self.transform = transform
        self.nb_samples = nb_samples

    def __len__(self):
        """
        Returns the length of the dataset.
        """
        return self.nb_samples

    def __iter__(self):
        for packet in self.packets:
            fields = get_traffic_vector(packet)
            
            yield fields
