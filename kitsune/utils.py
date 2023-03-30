# extract features
from FeatureExtractor import FE
from Transformation import Transformation, generate_key
import os

#pcap file to features tsv using wireshark
def packet_parser(pcap_file, output_file):
    command = "tshark -r {} -T fields -e frame.time_epoch -e frame.len -e frame.protocols -e ip.src -e ip.dst -e ip.proto -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e dns.qry.name -e dns.qry.type -e dns.resp.name -e dns.resp.type -e dns.flags.response -e dns.flags.rcode -e dns.flags.recursion_desired -e dns.flags.recursion_available -e dns.flags.check_disable -e dns.flags.authentic_data -e dns.flags.truncated -e dns.flags.z -e dns.flags.authentic_data -e dns.flags.check_disable -e dns.flags.recursion_available -e dns.flags.recursion_desired -e dns.flags.rcode -e dns.flags.response -e dns.resp.type -e dns.resp.name -e dns.qry.type -e dns.qry.name -e udp.dstport -e udp.srcport -e tcp.dstport -e tcp.srcport -e ip.proto -e ip.dst -e ip.src -e frame.protocols -e frame.len -e frame.time_epoch > {}".format(pcap_file, output_file)
    os.system(command)

def extract_features(data_path, output_path):
    max_vec = [-1]*100
    min_vec = [1e10]*100
    fe = FE(data_path)   
    while True:
        fv = fe.get_next_vector()
        if len(fv) == 0:
            break
        for i in range(len(fv)):
            if fv[i] > max_vec[i]:
                max_vec[i] = fv[i]
            if fv[i] < min_vec[i]:
                min_vec[i] = fv[i]

    fe = FE(data_path)
    f = open(output_path, "w")
    while True:
        fv = fe.get_next_vector()
        if len(fv) == 0:
            break
        for i in range(len(fv)):
            fv[i] = (fv[i] - min_vec[i]) / (max_vec[i] - min_vec[i])
        f.write(",".join([str(x) for x in fv]) + "\n")

    f.close()



def transform_features():
    key = generate_key(32)
    t = Transformation("1", key)

