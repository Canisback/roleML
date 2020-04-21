import roleml
import json
import os

def test_fix__nofix_1():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
        
    fixed_data, fixed_timeline = roleml.fix_and_augment_game_and_timeline(data, data["timeline"])
    
    for k, p in enumerate(data["participants"]):
        assert p["timeline"] == fixed_data["participants"][k]["timeline"]

def test_fix__nofix_2():
    with open(os.path.dirname(__file__) + "/data/EUW-3692606327.json", "r") as f:
        data = json.load(f)
        
    fixed_data, fixed_timeline = roleml.fix_and_augment_game_and_timeline(data, data["timeline"])
    
    for k, p in enumerate(data["participants"]):
        assert p["timeline"] == fixed_data["participants"][k]["timeline"]
        
        #Does not upgrade participant
        assert not "role" in p
        assert not "goldDiffPerMinDeltas" in p["timeline"]
        
#No test for single fix as I did not find a single game where Riot was wrong and roleml had a full roster on both sides



def test_fix_upgrade_participant_1():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
        
    fixed_data, fixed_timeline = roleml.fix_and_augment_game_and_timeline(data, data["timeline"], True)
    
    for p in fixed_data["participants"]:
        assert "role" in p
        
def test_fix_upgrade_participant_2():
    with open(os.path.dirname(__file__) + "/data/EUW-3692606327.json", "r") as f:
        data = json.load(f)
        
    fixed_data, fixed_timeline = roleml.fix_and_augment_game_and_timeline(data, data["timeline"], True)
    
    for p in fixed_data["participants"]:
        assert "role" in p
        assert "goldDiffPerMinDeltas" in p["timeline"]

        
def test_fix_upgrade_timeline_1():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
        
    fixed_data, fixed_timeline = roleml.fix_and_augment_game_and_timeline(data, data["timeline"], False, True)
    
    for p in fixed_data["participants"]:
        assert not "role" in p
        assert not "goldDiffPerMinDeltas" in p["timeline"]
    
    for frame in fixed_timeline["frames"]:
        for k, p in frame["participantFrames"].items():
            assert "totalGoldDiff" in p
            assert "xpDiff" in p
            assert "minionsKilledDiff" in p
            assert "jungleMinionsKilledDiff" in p

        
def test_fix_upgrade_timeline_2():
    with open(os.path.dirname(__file__) + "/data/EUW-3692606327.json", "r") as f:
        data = json.load(f)
        
    fixed_data, fixed_timeline = roleml.fix_and_augment_game_and_timeline(data, data["timeline"], False, True)
    
    for p in fixed_data["participants"]:
        assert not "role" in p
        assert not "goldDiffPerMinDeltas" in p["timeline"]
    
    for frame in fixed_timeline["frames"]:
        for k, p in frame["participantFrames"].items():
            assert "totalGoldDiff" in p
            assert "xpDiff" in p
            assert "minionsKilledDiff" in p
            assert "jungleMinionsKilledDiff" in p

        
def test_fix_upgrade_participant_and_timeline_1():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
        
    fixed_data, fixed_timeline = roleml.fix_and_augment_game_and_timeline(data, data["timeline"], True, True)
    
    for p in fixed_data["participants"]:
        assert "role" in p
        assert "goldDiffPerMinDeltas" in p["timeline"]
    
    for frame in fixed_timeline["frames"]:
        for k, p in frame["participantFrames"].items():
            assert "totalGoldDiff" in p
            assert "xpDiff" in p
            assert "minionsKilledDiff" in p
            assert "jungleMinionsKilledDiff" in p

        
def test_fix_upgrade_participant_and_timeline_2():
    with open(os.path.dirname(__file__) + "/data/EUW-3692606327.json", "r") as f:
        data = json.load(f)
        
    fixed_data, fixed_timeline = roleml.fix_and_augment_game_and_timeline(data, data["timeline"], True, True)
    
    for p in fixed_data["participants"]:
        assert "role" in p
        assert "goldDiffPerMinDeltas" in p["timeline"]
    
    for frame in fixed_timeline["frames"]:
        for k, p in frame["participantFrames"].items():
            assert "totalGoldDiff" in p
            assert "xpDiff" in p
            assert "minionsKilledDiff" in p
            assert "jungleMinionsKilledDiff" in p
            
            
def test_fix_opponent_not_found_1():
    with open(os.path.dirname(__file__) + "/data/EUW-4233525244.json", "r") as f:
        data = json.load(f)
        
    try:
        fixed_data, fixed_timeline = roleml.fix_and_augment_game_and_timeline(data, data["timeline"])
        assert False
    except:
        assert True