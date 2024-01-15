import os
from tardigrade import KitsuneIDS
from tardigrade.utils.metrics import *
import numpy as np

benign_file = "tardigrade/ids/Data/weekday"
benign_netstat = "tardigrade/ids/Data/[Normal]Google_Home_Mini.pkl"
 
# Parsing of the data.
model = KitsuneIDS()
num_packets = model.feature_extractor(benign_file , save_netstat=benign_netstat)
 
 
# Training of the model.
 
# kitsune_path = "tardigrade/ids/kitsune_ids/models/kitsune.pkl"
 
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
    # "model_path": kitsune_path,
    # if normalize==true then kitsune does normalization automatically
    "normalize": True
}
 
model.train_model(train_params)
 

 
malicious_traffic_plot = "port_scan.png"
benign_traffic_plot = "benign.png"
 
 
malicious_file = "tardigrade/ids/Data/Adv_ARP_Spoofing_Google-Nest-Mini_1"
model.feature_extractor(malicious_file,save_netstat=benign_netstat)
 
# malicious_file = "tardigrade/ids/Data/port_scan_attack_only"
# kitsune_threshold = "_kitsune_threshold.csv"
 
# benign_pos , kitsune_threshold = model.test_model(out_image=benign_traffic_plot,record_scores=True)
 
mal_pos, mal_threshold = model.test_model(malicious_file , out_image=malicious_traffic_plot,record_scores=True)

print("port scan examples over threshold:", mal_pos)
 
 

