from roleml import roleml
import json
import os

def test_get_stats_1():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
        
    stats_at_10 = {
        1: {'minionsKilled': 2, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        2: {'minionsKilled': 7, 'jungleMinionsKilled': 44, 'jungleMinionRatio': 0.8627450980392157},
        3: {'minionsKilled': 49, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        4: {'minionsKilled': 50, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        5: {'minionsKilled': 34, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        6: {'minionsKilled': 56, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        7: {'minionsKilled': 47, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        8: {'minionsKilled': 12, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        9: {'minionsKilled': 1, 'jungleMinionsKilled': 35, 'jungleMinionRatio': 0.9722222222222222},
        10: {'minionsKilled': 58, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0}
    }
    
    assert stats_at_10 == roleml.get_stats_at_10(data["timeline"])

def test_get_stats_2():
    with open(os.path.dirname(__file__) + "/data/EUW-3692606327.json", "r") as f:
        data = json.load(f)
        
    stats_at_10 = {
        1: {'minionsKilled': 3, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        2: {'minionsKilled': 63, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        3: {'minionsKilled': 59, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        4: {'minionsKilled': 12, 'jungleMinionsKilled': 44, 'jungleMinionRatio': 0.7857142857142857},
        5: {'minionsKilled': 78, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        6: {'minionsKilled': 70, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        7: {'minionsKilled': 11, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        8: {'minionsKilled': 48, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0},
        9: {'minionsKilled': 1, 'jungleMinionsKilled': 40, 'jungleMinionRatio': 0.975609756097561},
        10: {'minionsKilled': 46, 'jungleMinionsKilled': 0, 'jungleMinionRatio': 0.0}
    }
    
    assert stats_at_10 == roleml.get_stats_at_10(data["timeline"])