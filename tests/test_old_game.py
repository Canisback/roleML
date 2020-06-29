import logging

import pytest

import roleml


def test_old_game_pro(pro_game, caplog):
    with caplog.at_level(logging.WARNING):
        roleml.predict(pro_game["game"], pro_game["game"]["timeline"])

    assert caplog.text


def test_recent_game(clean_game_na):
    with pytest.warns(None) as record:
        roleml.predict(clean_game_na["game"], clean_game_na["game"]["timeline"])

    assert not record
