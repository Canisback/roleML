from roleml.features import _get_stats_at_10


def test_get_stats_na(clean_game_na):
    assert clean_game_na["stats_at_10"] == _get_stats_at_10(clean_game_na["game"]["timeline"])


def test_get_stats_euw(clean_game_euw):
    assert clean_game_euw["stats_at_10"] == _get_stats_at_10(clean_game_euw["game"]["timeline"])
