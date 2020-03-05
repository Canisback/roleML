from roleml import roleml
import json
import os
import pandas

def test_get_features_1():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
        
    features = pandas.read_csv(os.path.dirname(__file__) + "/data/NA-3023745286_features.csv")
    
    assert features.equals(roleml.get_features(data, data["timeline"]))

def test_get_features_2():
    with open(os.path.dirname(__file__) + "/data/EUW-3692606327.json", "r") as f:
        data = json.load(f)
        
    features = pandas.read_csv(os.path.dirname(__file__) + "/data/EUW-3692606327_features.csv")
    print(features.index)
    print(roleml.get_features(data, data["timeline"]).index)
    print(features.columns)
    print(roleml.get_features(data, data["timeline"]).columns)
    
    assert features.equals(roleml.get_features(data, data["timeline"]))