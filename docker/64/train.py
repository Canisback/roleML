import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedShuffleSplit

df = pd.read_csv("dataset/dataset_participants2.csv")

target = df["position"]
data = df.drop(["position", "participantId", "gameId"], axis=1)

shuffle_split = StratifiedShuffleSplit(train_size=0.9, n_splits=10)

c = RandomForestClassifier(min_samples_split=5, n_estimators=100)

print("Begin training")

accs = []

for train_index, test_index in shuffle_split.split(data, target):
    c.fit(data.iloc[train_index], target.iloc[train_index])
    accs.append(accuracy_score(target[test_index], c.predict(data.iloc[test_index])))

print("splits accuracy : ", accs)
print("mean accuracy : ", sum(accs) / len(accs))

dfEntries = pd.read_csv("dataset/dataset_verification.csv")

dfEntries["position_prediction"] = c.predict(
    dfEntries.drop(["position", "participantId", "gameId", "position_verified"], axis=1)
)

dfWorkingEntries = dfEntries[["gameId", "participantId", "position", "position_prediction", "position_verified"]]

print(
    "Verification errors : ",
    dfWorkingEntries[dfWorkingEntries["position_prediction"] != dfWorkingEntries["position_verified"]].shape[0],
)

joblib.dump(c, "model/role_identification_model_64bits.sav")
