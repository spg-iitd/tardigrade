import os
import pickle
from tardigrade.ids import KitsuneIDS
from tardigrade.utils.metrics import *
import numpy as np

benign_file = "./utils/Data/weekday_20k"

model = KitsuneIDS(keep_csv=False)
num_packets = model.feature_extractor(benign_file, add_label=True)

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
 
threshold = model.train_model(train_params)
print(f"Threshold is: {threshold}")