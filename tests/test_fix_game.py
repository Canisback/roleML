import pytest

import roleml


def test_fix(clean_game_na):
    fixed_data, fixed_timeline = roleml.fix_game(clean_game_na["game"], clean_game_na["game"]["timeline"])

    for p in fixed_data["participants"]:
        assert "role" in p


def test_fix_no_timeline(clean_game_na):
    fixed_data, fixed_timeline = roleml.fix_game(clean_game_na["game"], clean_game_na["game"]["timeline"])

    for k, p in enumerate(clean_game_na["game"]["participants"]):
        assert p["timeline"] == fixed_data["participants"][k]["timeline"]


def test_fix_full(clean_game_na):
    fixed_data, fixed_timeline = roleml.fix_game(
        clean_game_na["game"], clean_game_na["game"]["timeline"], fix_timeline=True
    )

    for frame in fixed_timeline["frames"]:
        for k, p in frame["participantFrames"].items():
            assert "totalGoldDiff" in p
            assert "xpDiff" in p
            assert "minionsKilledDiff" in p
            assert "jungleMinionsKilledDiff" in p


def test_opponent_not_found(opponent_not_found_game):
    with pytest.raises(roleml.exceptions.NoOpponentFoundException):
        roleml.fix_game(opponent_not_found_game["game"], opponent_not_found_game["game"]["timeline"], fix_timeline=True)
