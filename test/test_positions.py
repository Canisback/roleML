from roleml import roleml
import json
import os

def test_get_positions_1():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
    
    participants_positions = {
        1: ['jungle', 'bot', 'bot', 'bot', 'bot', 'bot', 'jungle', 'bot', 'bot', 'bot'],
        2: ['jungle', 'jungle', 'jungle', 'jungle', 'bot', 'jungle', None, 'jungle', 'jungle', 'top'],
        3: ['top', 'top', 'jungle', 'top', 'top', 'top', 'top', 'top', 'top', 'top'],
        4: [None, 'bot', 'bot', 'bot', 'bot', 'bot', 'bot', 'bot', 'bot', 'bot'],
        5: [None, 'mid', 'jungle', 'mid', None, 'mid', 'mid', 'mid', None, 'mid'],
        6: ['top', 'top', 'top', 'jungle', 'top', 'top', 'top', 'jungle', 'top', 'top'],
        7: ['jungle', 'bot', 'bot', 'bot', None, 'bot', 'bot', 'bot', 'bot', 'bot'],
        8: ['jungle', 'bot', 'bot', 'bot', 'bot', 'bot', None, 'bot', 'bot', 'bot'],
        9: ['jungle', 'jungle', 'jungle', 'jungle', 'jungle', 'jungle', 'jungle', 'top', 'jungle', 'jungle'],
        10: ['jungle', 'mid', 'mid', 'mid', 'mid', 'mid', 'mid', 'mid', None, 'mid']
    }
    
    assert roleml.get_positions(data["timeline"]) == participants_positions
    
def test_get_lane_frequencies_1():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
        
    lane_frequency = {
        1: {'bot': 8, 'jungle': 2, 'mid': 0, 'top': 0},
        2: {'jungle': 7, 'bot': 1, 'top': 1, 'mid': 0},
        3: {'top': 9, 'jungle': 1, 'mid': 0, 'bot': 0},
        4: {'bot': 9, 'jungle': 0, 'mid': 0, 'top': 0},
        5: {'mid': 6, 'jungle': 1, 'top': 0, 'bot': 0},
        6: {'top': 8, 'jungle': 2, 'mid': 0, 'bot': 0},
        7: {'bot': 8, 'jungle': 1, 'mid': 0, 'top': 0},
        8: {'bot': 8, 'jungle': 1, 'mid': 0, 'top': 0},
        9: {'jungle': 9, 'top': 1, 'bot': 0, 'mid': 0},
        10: {'mid': 8, 'jungle': 1, 'top': 0, 'bot': 0}
    }
    
    assert roleml.get_lane_frequencies(roleml.get_positions(data["timeline"])) == lane_frequency
    
def test_get_most_frequent_lane_1():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
    
    most_frequent = {
        1: 'bot',
        2: 'jungle',
        3: 'top',
        4: 'bot',
        5: 'mid',
        6: 'top',
        7: 'bot',
        8: 'bot',
        9: 'jungle',
        10: 'mid'
    }
    
    assert roleml.get_most_frequent_lane(roleml.get_positions(data["timeline"])) == most_frequent
    