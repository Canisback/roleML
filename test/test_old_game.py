import roleml
import json
import os
import pytest


def test_old_game_1():
    with open(os.path.dirname(__file__) + "/data/TR1-266041574.json", "r") as f:
        data = json.load(f)
    
    with pytest.warns(UserWarning):
        roleml.predict(data, data["timeline"])
        
        


def test_not_old_game_1():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
        
    with pytest.warns(None) as record:
        roleml.predict(data, data["timeline"])
        
    assert not record