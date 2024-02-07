import os
import pickle
from tardigrade.ids import KitsuneIDS
from tardigrade.utils.metrics import *
import numpy as np

malicious_traffic_plot = "port_scan.png"
benign_traffic_plot = "benign.png"

model = KitsuneIDS()

# TODO: #absolute
model.threshold = 0.2724

infile = open("adv_sizes", "rb")
params = pickle.load(infile)
infile.close()


# malicious_file = "./adv_data/Adv_Port_Scanning_SmartTV"
# malicious_file = "./adv_data/ARP_Spoofing_Google-Nest-Mini_1"
malicious_file = "./adv_data/Port_Scanning_SmartTV"

model.feature_extractor(params["adv_sizes"], malicious_file)
 
# malicious_file = "tardigrade/ids/Data/port_scan_attack_only"
# kitsune_threshold = "_kitsune_threshold.csv"
 
# benign_pos , kitsune_threshold = model.test_model(out_image=benign_traffic_plot,record_scores=True)
 
score_array = model.test_model(malicious_file, out_image=malicious_traffic_plot, record_scores=False)

model.get_plot(score_array)
model.eval_metrics(score_array)