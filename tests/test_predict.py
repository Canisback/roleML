import pytest

import roleml
from roleml import exceptions


def test_predict_1(clean_game_na):
    assert clean_game_na["expected_roles"] == roleml.predict(clean_game_na["game"], clean_game_na["game"]["timeline"])


def test_predict_2(clean_game_euw):
    assert clean_game_euw["expected_roles"] == roleml.predict(clean_game_euw["game"], clean_game_euw["game"]["timeline"])


def test_predict_match_too_short(short_game):
    with pytest.raises(exceptions.MatchTooShort):
        roleml.predict(short_game["game"], short_game["game"]["timeline"])


def test_predict_match_aram(aram_game):
    with pytest.raises(exceptions.IncorrectMap):
        roleml.predict(aram_game["game"], aram_game["game"]["timeline"])

def test_predict_empty_lane_frequency(empty_lane_frequency_game):
    roleml.predict(empty_lane_frequency_game["game"], empty_lane_frequency_game["game"]["timeline"])
    assert True
    