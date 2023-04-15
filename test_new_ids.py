from tardigrade.kitsune import KitModel, KeyedKitModel
from tardigrade.kitsune import evaluation_metrics

# Test Kitsune

model = KitModel()

print("Training Kitsune model...")
model.train_model("data/traffic_less.csv")


print("Testing Kitsune model...")
scores = model.test("data/traffic_less.csv")

print(scores)



# Test Kitsune Keyed

model = KeyedKitModel()

print("Training Kitsune keyed model...")
model.train_model("data/traffic_less.csv")

print("Testing Kitsune keyed model...")
scores = model.test("data/traffic_less.csv")

print(scores)






