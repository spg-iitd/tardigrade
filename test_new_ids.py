import os
import pickle
from tardigrade.ids import KitsuneIDS
from tardigrade.utils.metrics import *
import numpy as np

malicious_traffic_plot = "port_scan.png"
benign_traffic_plot = "benign.png"

model = KitsuneIDS(keep_csv=True)

# TODO: #absolute
model.threshold = 0.24759

# malicious_file = "./adv_data/Adv_Port_Scanning_SmartTV"
# malicious_file = "./adv_data/ARP_Spoofing_Google-Nest-Mini_1"
malicious_file = "../PANDA/PANDA/data/malicious/Port_Scanning_SmartTV"
# malicious_file = "../PANDA/PANDA/data/adversarial/fgsm/Adv_ARP_Spoofing_Google-Nest-Mini_1"
# malicious_file = "../PANDA/PANDA/data/adversarial/fgsm/Adv_UDP_Flooding_Lenovo_Bulb_1"
# malicious_file = "./utils/Data/weekday_20k"
# model.feature_extractor(malicious_file)
score_array = model.test_model(malicious_file, out_image=malicious_traffic_plot, record_scores=False)

model.get_plot(score_array)
model.eval_metrics(score_array)
