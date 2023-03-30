import torch
import utils
import operator
import torchdata.datapipes.iter as it
from models import Kitsune
from FeatureExtractor import FE
from data import FileFormat, build_input_data_pipe
from engine import build_feature_mapper, train_single_epoch, predict

class KitModel:
    def __init__(self):
        self.fm = None
        self.model = None
        self.optimizer = None
        self.dp = None

    # extract features
    def extract_features(self, data_path, output_path):
        fe = FE(data_path)
        count = 0
        with open(output_path, "w") as f:
            while True:
                fv = fe.get_next_vector()
                if len(fv) == 0:
                    break
                fv = [str(x) for x in fv]
                f.write(",".join(fv) + "\n")
                count = count+1

                if count%100000 == 0:
                    print("Processed {} packets".format(count))

        f.close()

    # Generate Data
    def gen_dp(self, data_path):
        return build_input_data_pipe(
            data_path, batch_size=32, shuffle=True, file_format=FileFormat.csv)

    # feature mapper
    def map_features(self):
        return build_feature_mapper(self.dp, 100)

    # load and store model
    def load_model(self, model_path):
        self.model = Kitsune.from_pretrained(model_path)

    def store_model(self, model_path):
        self.model.save(model_path)

    def score(self, x):
        return self.model.score(x)

    # train model
    def train_model(self, input_path: str,
                    batch_size: int = 32,
                    file_format: FileFormat = "csv",
                    compression_rate: float = 0.6):

        # Build data pipe
        self.dp = self.gen_dp(input_path)

        # Build feature mapper
        self.fm = self.map_features()

        # Build model
        self.model = Kitsune(feature_mapper=self.fm,
                        compression_rate=compression_rate)
        
        # Build optimizer
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=1e-3)
        
        
        # TODO: take epoch as input
        for epoch in range(1):
            train_single_epoch(
                self.model, self.dp, self.optimizer, epoch=epoch)
        

    # test model
    def test(self, input_path: str, batch_size: int = 32, file_format: FileFormat = "csv"):
        test_data = self.gen_dp(input_path)

        # test_data = torch.randn(16, 128)
        
        scores = predict(self.model, test_data)

        return scores




if __name__ == "__main__":
    data = "Data/traffic_less.csv"

    # # Extract features
    # print("Extracting features")
    # model = KitModel()
    # model.extract_features("Data/traffic.tsv", "Data/traffic.csv")

    # Train model on "../Data/traffic.csv"
    print("Training model on " + data)
    model = KitModel()

    # Train model
    model.train_model(data)
    print("Training complete")

    # Store model
    model.store_model("kitsune.pt")

    # Test model on "../Data/traffic.csv"
    print("Testing model on " + data)
    testModel = KitModel()

    # Load model
    testModel.load_model("kitsune.pt")

    # Test model
    scores = testModel.test(data)
    print("Testing complete")

    # Save scores
    print("Saving scores")
    with open("scores.txt", "w") as f:
        for score in scores:
            f.write(str(score) + "\n")
    print("Scores saved")




