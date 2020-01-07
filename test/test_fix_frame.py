from roleml import roleml
import json
import os

def is_key_participantId_same(frame):
    result = True
    for k, v in frame["participantFrames"].items():
        if not k == str(v["participantId"]):
            result = False
    return result

def test_fix_frame_unordered():
    with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
        data = json.load(f)
    
    for frame in data["timeline"]["frames"]:
        assert not is_key_participantId_same(frame)
    
    for frame in data["timeline"]["frames"]:
        assert is_key_participantId_same(roleml.fix_frame(frame))

def test_fix_frame_ordered():
    with open(os.path.dirname(__file__) + "/data/EUW-3692606327.json", "r") as f:
        data = json.load(f)
    
    for frame in data["timeline"]["frames"]:
        assert is_key_participantId_same(frame)
    
    for frame in data["timeline"]["frames"]:
        assert is_key_participantId_same(roleml.fix_frame(frame))
    