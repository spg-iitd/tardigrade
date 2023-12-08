# from kitsune_ids import parse_with_kitsune as p
# create a class AwesomeIDS that would have the parse fuction that basically the calls the parse_kitsune function from the parse_with_kitsune.py file 
# and then import the AwesomeIDS class in the __init__.py file and then call the parse function from the AwesomeIDS class in the __init__.py file

# from ..kitsune_ids import parse_with_kitsune

from ..kitsune_ids import parse_with_kitsune
from ..kitsune_ids.kitsune import *

# class AwesomeIDS:
#     """
#     This is an awesome IDS
#     """
#     def parse (self,pcap_file, output_file_name, add_label=False, write_prob=1, count=float('Inf'), parse_type="scapy", netstat_path=None, save_netstat=None, add_proto=False, add_time=False, netstat_log_file=None):
#         parse_with_kitsune.parse_kitsune(pcap_file, output_file_name, add_label, write_prob, count, parse_type, netstat_path, save_netstat, add_proto, add_time, netstat_log_file)

class AwesomeIDS:
    """
    This is an awesome IDS
    """
    # This is for parsing the data and extracting the features from the data .
    def parse (self,pcap_file, output_file_name, add_label=False, write_prob=1, count=float('Inf'), parse_type="scapy", netstat_path=None, save_netstat=None, add_proto=False, add_time=False, netstat_log_file=None):
        parse_with_kitsune.parse_kitsune(pcap_file, output_file_name, add_label, write_prob, count, parse_type, netstat_path, save_netstat, add_proto, add_time, netstat_log_file)

    # make a function that would train the model and then save the model in a file
    def train_model(self, params):
        train_normal(params) 

    def test_model(self, path, model_path, threshold=None, ignore_index=-1, out_image=None, meta_file=None, record_scores=False, y_true=None, record_prediction=False, load_prediction=False, plot_with_time=False):
        return eval_kitsune(path, model_path, threshold, ignore_index, out_image, meta_file, record_scores, y_true, record_prediction, load_prediction, plot_with_time)
