import roleml
from roleml import exceptions
import json
import os


def test_label_1():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
        
    roleml.set_label_type("rgapi")
    roles = {
        1: {'lane': 'BOTTOM', 'role': 'DUO_SUPPORT'},
        2: {'lane': 'JUNGLE', 'role': 'NONE'},
        3: {'lane': 'TOP', 'role': 'SOLO'},
        4: {'lane': 'BOTTOM', 'role': 'DUO_CARRY'},
        5: {'lane': 'MIDDLE', 'role': 'SOLO'},
        6: {'lane': 'TOP', 'role': 'SOLO'},
        7: {'lane': 'BOTTOM', 'role': 'DUO_CARRY'},
        8: {'lane': 'BOTTOM', 'role': 'DUO_SUPPORT'},
        9: {'lane': 'JUNGLE', 'role': 'NONE'},
        10: {'lane': 'MIDDLE', 'role': 'SOLO'}
    }
    
    assert roles == roleml.predict(data, data["timeline"])

def test_label_2():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
        
    roleml.set_label_type("full")
    roles = {
        1: 'BOTTOM_DUO_SUPPORT',
        2: 'JUNGLE_NONE',
        3: 'TOP_SOLO',
        4: 'BOTTOM_DUO_CARRY',
        5: 'MIDDLE_SOLO',
        6: 'TOP_SOLO',
        7: 'BOTTOM_DUO_CARRY',
        8: 'BOTTOM_DUO_SUPPORT',
        9: 'JUNGLE_NONE',
        10: 'MIDDLE_SOLO'
    }
    
    assert roles == roleml.predict(data, data["timeline"])

def test_label_3():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
        
    roleml.set_label_type("clean")    
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
    
    
def test_label_4():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
          
   
    try:
        roleml.set_label_type("test")  
        assert False
    except exceptions.WrongLabel:
        assert True
    except:
        assert False