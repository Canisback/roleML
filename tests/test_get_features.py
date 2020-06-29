import os

import pandas

from roleml.features import _get_features


def test_get_features_na(clean_game_na):
    features = pandas.read_csv(os.path.join(os.path.dirname(__file__), "data", "NA-3023745286_features.csv"))

    assert features.equals(_get_features(clean_game_na["game"], clean_game_na["game"]["timeline"]))


def test_get_features_euw(clean_game_euw):
    features = pandas.read_csv(os.path.join(os.path.dirname(__file__), "data", "EUW-3692606327_features.csv"))

    assert features.equals(_get_features(clean_game_euw["game"], clean_game_euw["game"]["timeline"]))
