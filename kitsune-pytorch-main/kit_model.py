import kitsune
import torch
import operator
import torchdata.datapipes.iter as it

'''
dp = it.IoPathFileLister("s3://bucket/dataset").filter(lambda p: p.endswith(".json"))
dp = FileOpener(dp, mode="r").parse_json_files().map(operator.itemgetter(1))
dp = dp.map(lambda jp: torch.as_tensor(jp["features"]))
dp = dp.batch(32).collate(torch.stack)

fm = kitsune.engine.build_feature_mapper(dp, ...)  # Fill with your parameters
model = kitsune.Kitsune(feature_mapper=fm)
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)
for epoch in range(10):
    kitsune.engine.train_single_epoch(model, dp, optimizer, epoch=epoch)

model.save("kitsune.pt")  # Keep it for later
'''

class KitModel:
    def __init__(self):
        self.fm = None
        self.model = None
        self.optimizer = None
        self.dp = None

    #please check
    def gen_dp(self, data_path):
        self.dp = it.IoPathFileLister(data_path).filter(lambda p: p.endswith(".json"))
        self.dp = FileOpener(self.dp, mode="r").parse_json_files().map(operator.itemgetter(1))
        self.dp = self.dp.map(lambda jp: torch.as_tensor(jp["features"]))
        self.dp = self.dp.batch(32).collate(torch.stack)

    #feature mapper
    def map_features(self):
        self.fm = kitsune.engine.build_feature_mapper(self.dp, ...) #other param

    #load and store model
    def load_model(self, model_path):
        self.model = kitsune.Kitsune.from_pretrained(model_path)

    def store_model(self, model_path):
        self.model.save(model_path)
    
    #train model
    def train_model(self, data_path):
        self.gen_dp(data_path)
        self.map_features()
        self.model = kitsune.Kitsune(feature_mapper=self.fm)
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=1e-3)
        for epoch in range(10):
            kitsune.engine.train_single_epoch(self.model, self.dp, self.optimizer, epoch=epoch)
    
    # this is wrong, need to fix
    def test():
        samples = torch.randn(16, 128)
        with torch.inference_mode():
            score = self.model(samples)
        