from roleml.roleml import _fix_frame_keys


def key_equals_participant_id(frame):
    return all(k == str(v["participantId"]) for k, v in frame["participantFrames"].items())


def test_fix_frame_unordered(clean_game_na):
    for frame in clean_game_na["game"]["timeline"]["frames"]:
        assert not key_equals_participant_id(frame)

    for frame in clean_game_na["game"]["timeline"]["frames"]:
        assert key_equals_participant_id(_fix_frame_keys(frame))


def test_fix_frame_ordered(clean_game_euw):
    for frame in clean_game_euw["game"]["timeline"]["frames"]:
        assert key_equals_participant_id(frame)

    for frame in clean_game_euw["game"]["timeline"]["frames"]:
        assert key_equals_participant_id(_fix_frame_keys(frame))
