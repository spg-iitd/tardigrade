# import AwesomeIDS class in test_new_ids.py and call the parse function from the AwesomeIDS class
import os
from tardigrade.ids.awesome_ids import AwesomeIDS
from tardigrade.utils.metrics import * 
import numpy as np
# from tardigrade.utils import evaluation_metrics

# # Test Kitsune
# model = KitModel()

# print("Training Kitsune model...")
# model.train_model("data/traffic_less.csv")

# print("Testing Kitsune model...")
# scores = model.test("data/traffic_less.csv")

# print(scores)

# # Test Kitsune Keyed
# model = KeyedKitModel()

# print("Training Kitsune keyed model...")
# model.train_model("data/traffic_less.csv")

# print("Testing Kitsune keyed model...")
# scores = model.test("data/traffic_less.csv")

# print(scores)
benign_file = "tardigrade/ids/Data/[Normal]Google_Home_Mini"
benign_netstat = "tardigrade/ids/Data/[Normal]Google_Home_Mini.pkl"

# Parsing of the data.
model = AwesomeIDS()
model.parse(benign_file + ".pcap", benign_file + ".csv",
              add_label=False, parse_type="scapy", add_proto=True, add_time=True, save_netstat=benign_netstat)


# Training of the model.

kitsune_path = "tardigrade/ids/kitsune_ids/models/kitsune.pkl"

num_packets = 14400
train_params = {
    # the pcap, pcapng, or tsv file to process.
    "path": benign_file + ".csv",
    "packet_limit": np.Inf,  # the number of packets to process,

    # KitNET params:
    # maximum size for any autoencoder in the ensemble layer
    "maxAE": 10,
    # the number of instances taken to learn the feature mapping (the ensemble's architecture)
    "FMgrace": np.floor(0.2 * num_packets),
    # the number of instances used to train the anomaly detector (ensemble itself)
    # FMgrace+ADgrace<=num samples in normal traffic
    "ADgrace": np.floor(0.8 * num_packets),
    # directory of kitsune
    "model_path": kitsune_path,
    # if normalize==true then kitsune does normalization automatically
    "normalize": True
}

model.train_model(train_params)


# Testing of the model.

# attack_plot_base_path = "/port_scan.png"
# if not os.path.exists(attack_plot_base_path):
#     os.makedirs(attack_plot_base_path)

malicious_traffic_plot = "port_scan.png"
benign_traffic_plot = "benign.png"
malicious_file = "tardigrade/ids/Data/port_scan_attack_only"
kitsune_threshold = "_kitsune_threshold.csv"

benign_pos , kitsune_threshold = model.test_model(benign_file + ".csv" , kitsune_path,
                          threshold=None, out_image=benign_traffic_plot,record_scores=True)

mal_pos, mal_threshold = model.test_model(malicious_file + ".csv" , kitsune_path,
                          threshold=kitsune_threshold, out_image=malicious_traffic_plot,record_scores=True)
print("port scan examples over threshold:", mal_pos)



# Evaluation of the model.

# scores_path = '_kitsune_score.csv'
# threshold_path = '_kitsune_threshold.csv'

# print("Evaluation metrics for Kitsune: ")
# evaluation_metrics(scores_path, threshold_path)