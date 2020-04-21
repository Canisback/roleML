import roleml
from roleml import exceptions
import json
import os


def test_predict_1():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
        
    roles = {
        1: 'supp',
        2: 'jungle',
        3: 'top',
        4: 'bot',
        5: 'mid',
        6: 'top',
        7: 'bot',
        8: 'supp',
        9: 'jungle',
        10: 'mid'
    }
    
    assert roles == roleml.predict(data, data["timeline"])


def test_predict_2():
    with open(os.path.dirname(__file__) + "/data/EUW-3692606327.json", "r") as f:
        data = json.load(f)
        
    roles = {
        1: 'supp',
        2: 'top',
        3: 'mid',
        4: 'jungle',
        5: 'bot',
        6: 'top',
        7: 'supp',
        8: 'mid',
        9: 'jungle',
        10: 'bot'
    }
    
    assert roles == roleml.predict(data, data["timeline"])

def test_predict_match_too_short():
    with open(os.path.dirname(__file__) + "/data/EUW-4236896092.json", "r") as f:
        data = json.load(f)
    try:
        roleml.predict(data, data["timeline"])
        assert False
    except exceptions.MatchTooShort:
        assert True
    except:
        assert False

def test_predict_match_ARAM():
    with open(os.path.dirname(__file__) + "/data/EUW-4458819927.json", "r") as f:
        data = json.load(f)
    try:
        roleml.predict(data, data["timeline"])
        assert False
    except exceptions.IncorrectMap:
        assert True
    except:
        assert False