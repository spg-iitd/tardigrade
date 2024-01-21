import torch
import operator
import torchdata.datapipes.iter as it

from .data import FileFormat, build_input_data_pipe


from .models import Kitsune
from .data import FileFormat, build_input_data_pipe
from .engine import build_feature_mapper, train_single_epoch, predict

class KitModel:
    def __init__(self):
        self.fm = None
        self.model = None
        self.optimizer = None
        self.dp = None

    # Generate Data
    def __gen_dp__(self, data_path):
        return build_input_data_pipe(
            data_path, batch_size=32, shuffle=True, file_format=FileFormat.csv)

    # feature mapper
    def __map_features__(self):
        return build_feature_mapper(self.dp, 100)

    # load and store model
    def load_model(self, model_path:str):
        self.model = Kitsune.from_pretrained(model_path)

    def store_model(self, model_path:StopAsyncIteration()):
        self.model.save(model_path)

    def score(self, x: torch.Tensor):
        return self.model.score(x)

    # train model
    def train_model(self, input_path: str,
                    batch_size: int = 32,
                    file_format: FileFormat = "csv",
                    compression_rate: float = 0.6):

        # Build data pipe
        self.dp = self.__gen_dp__(input_path)

        # Build feature mapper
        self.fm = self.__map_features__()

        # Build model
        self.model = Kitsune(feature_mapper=self.fm,
                        compression_rate=compression_rate)
        
        # Build optimizer
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=1e-3)
        
        
        # TODO: take epoch as input
        for epoch in range(10):
            train_single_epoch(
                self.model, self.dp, self.optimizer, epoch=epoch)
        

    # test model
    def test(self, input_path: str, batch_size: int = 32, file_format: FileFormat = "csv"):
        test_data = self.__gen_dp__(input_path)   
        scores = predict(self.model, test_data)

        return scores
