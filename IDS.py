"""
    Parent class IDS
"""

from FeatureExtractor import *

class IDS:
    def __init__(self):
        # Initialize the IDS (Model)
        pass

    def forward(self, packet):
        # Process the packet and return the anomaly score
        pass

    def train(self, path_to_training_data):
        # Train the IDS
        pass

    def test(self, path_to_test_data):
        # Test the IDS
        pass

    

    
    