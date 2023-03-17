# MIT License
#
# Copyright (c) 2018 Yisroel mirsky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# class Kitsune:
#     def __init__(self,file_path,limit,max_autoencoder_size=10,FM_grace_period=None,AD_grace_period=10000,learning_rate=0.1,hidden_ratio=0.75,):
#         #init packet feature extractor (AfterImage)
#         self.FE = FE(file_path,limit)

#         #tranform the feature vector
#         self.key = generate_key(int(self.FE.get_num_features()/2))
#         self.Transformation = Transformation("1", self.key)

#         #init Kitnet
#         self.AnomDetector = KitNET(self.FE.get_num_features(),max_autoencoder_size,FM_grace_period,AD_grace_period,learning_rate,hidden_ratio)

#     def proc_next_packet(self):
#         # create feature vector
#         x = self.FE.get_next_vector()
        
#         if len(x) == 0:
#             return -1 #Error or no packets left

#         # transform feature vector
#         x = self.Transformation.transform(x)

#         # process KitNET
#         return self.AnomDetector.process(x)  # will train during the grace periods, then execute on all the rest.


from KitNET.KitNET import KitNET
from Transformation import *

"""
    Kitsune is child class of IDS.
"""

from Tardigrade.FeatureExtractor import FE
from Tardigrade.IDS import IDS

class Kitsune(IDS):
    def __init__(self,file_path,limit,max_autoencoder_size=10,FM_grace_period=None,AD_grace_period=10000,learning_rate=0.1,hidden_ratio=0.75,):
        # Kitsune attributes
        self.limit = limit
        self.max_autoencoder_size = max_autoencoder_size
        self.FM_grace_period = FM_grace_period
        self.AD_grace_period = AD_grace_period
        self.learning_rate = learning_rate
        self.hidden_ratio = hidden_ratio
        
        #init packet feature extractor (AfterImage)
        self.FE = FE(file_path,limit)

        #tranform the feature vector
        self.key = generate_key(int(self.FE.get_num_features()/2))
        self.Transformation = Transformation("1", self.key)

        #init Kitnet
        self.AnomDetector = KitNET(self.FE.get_num_features(),max_autoencoder_size,FM_grace_period,AD_grace_period,learning_rate,hidden_ratio)

        # Model Results
        self.train_results = []
        self.test_results = []


    def forward(self, x):
        # Forward pass
        pass

    def train(self):
        # Train the IDS
        for i in range(self.FM_grace_period + self.AD_grace_period):
            self.train_results.append(self.proc_next_packet())
        

    def test(self, threshold):
        # Test the IDS
        while(True):
            res = self.proc_next_packet()
            if res == -1:
                break
            self.test_results.append(res)

    def proc_next_packet(self):
        # create feature vector
        x = self.FE.get_next_vector()
        
        if len(x) == 0:
            return -1
        
        # process KitNET
        return self.AnomDetector.process(x)  # will train during the grace periods, then execute on all the rest.
    


