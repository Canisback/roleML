from roleml.features import _get_positions, _get_lane_frequencies, _get_most_frequent_lane


def test_get_positions_na(clean_game_na):
    assert _get_positions(clean_game_na["game"]["timeline"]) == clean_game_na["participants_positions"]


def test_get_lane_frequencies_1(clean_game_na):
    assert _get_lane_frequencies(_get_positions(clean_game_na["game"]["timeline"])) == clean_game_na["lane_frequency"]


def test_get_most_frequent_lane_1(clean_game_na):
    assert (
        _get_most_frequent_lane(_get_positions(clean_game_na["game"]["timeline"]))
        == clean_game_na["most_frequent_lane"]
    )
