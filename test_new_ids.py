import os
import pickle
from tardigrade.ids import KitsuneIDS
from tardigrade.utils.metrics import *
import numpy as np

benign_file = "./utils/Data/weekday"
# benign_netstat = "./utils/Data/[Normal]Google_Home_Mini.pkl"

infile = open("adv_sizes", "rb")
params = pickle.load(infile)
infile.close()

# Parsing of the data.
model = KitsuneIDS()
num_packets = model.feature_extractor(params["adv_sizes"], benign_file)
 
 
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
 
threshold = model.train_model(train_params)
print(threshold)
# from tardigrade.datasets import UQIoTDataset, CICFlowMeterDataset
# from tardigrade.ids import KitsuneIDS, FeCoIDs, DecisionTreeIDS

# IDS:
# Step 1: Model creation
# Step 2: Model training
# Step 3: Evaluation
# Step 4: Plotting and other extra things