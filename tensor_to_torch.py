import pickle
import torch

import torch.nn as nn

# 1. Read the model and figure out the architecture
with open("kitsune.pkl", "rb") as f:
    numpy_model = pickle.load(f)

weights = numpy_model.get_params()

import torch
from torch import nn

class Autoencoder(nn.Module):
    def __init__(self, W, hbias, vbias):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Linear(W.shape[0], W.shape[1], bias=True)
        self.encoder.weight.data = torch.from_numpy(W)
        self.encoder.bias.data = torch.from_numpy(hbias)
        self.decoder = nn.Linear(W.shape[1], W.shape[0], bias=True)
        self.decoder.weight.data = torch.from_numpy(W.T)
        self.decoder.bias.data = torch.from_numpy(vbias)

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

class KitNET(nn.Module):
    def __init__(self, tail_weights, head_weight):
        super(KitNET, self).__init__()

        # add the tails of the autoencoders
        self.tails = nn.ModuleList([Autoencoder(weight['W'], weight['hbias'], weight['vbias']) for weight in tail_weights])

        # add the head of the autoencoder
        self.head = Autoencoder(head_weight['W'], head_weight['hbias'], head_weight['vbias'])

    def forward(self, x):
        x = x.view(-1, 100)

        x_clusters = [
            torch.index_select(x, 1, torch.tensor(c)) for c in clusters
        ]

        tail_losses = []
        for tail, c in zip(self.tails, x_clusters):
            output = tail(c)
            loss = torch.log(self.rmse(output, c))
            tail_losses.append(loss)
        
        tails = torch.stack(tail_losses)
        x = self.head(tails)

        return x, tails

model = KitNET(weights["ensemble"], weights["output"])
print(model)

# save the model
torch.save(model.state_dict(), "kitsune.pth")
