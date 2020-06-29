import pytest

import roleml
from roleml import exceptions


def test_label_riot_api(clean_game_na):
    roleml.change_role_formatting("rgapi")
    roles = {
        1: {"lane": "BOTTOM", "role": "DUO_SUPPORT"},
        2: {"lane": "JUNGLE", "role": "NONE"},
        3: {"lane": "TOP", "role": "SOLO"},
        4: {"lane": "BOTTOM", "role": "DUO_CARRY"},
        5: {"lane": "MIDDLE", "role": "SOLO"},
        6: {"lane": "TOP", "role": "SOLO"},
        7: {"lane": "BOTTOM", "role": "DUO_CARRY"},
        8: {"lane": "BOTTOM", "role": "DUO_SUPPORT"},
        9: {"lane": "JUNGLE", "role": "NONE"},
        10: {"lane": "MIDDLE", "role": "SOLO"},
    }

    assert roles == roleml.predict(clean_game_na["game"], clean_game_na["game"]["timeline"])


def test_label_full(clean_game_na):
    roleml.change_role_formatting("full")
    roles = {
        1: "BOTTOM_DUO_SUPPORT",
        2: "JUNGLE_NONE",
        3: "TOP_SOLO",
        4: "BOTTOM_DUO_CARRY",
        5: "MIDDLE_SOLO",
        6: "TOP_SOLO",
        7: "BOTTOM_DUO_CARRY",
        8: "BOTTOM_DUO_SUPPORT",
        9: "JUNGLE_NONE",
        10: "MIDDLE_SOLO",
    }

    assert roles == roleml.predict(clean_game_na["game"], clean_game_na["game"]["timeline"])


def test_label_clean(clean_game_na):
    roleml.change_role_formatting("clean")

    roles = {
        1: "supp",
        2: "jungle",
        3: "top",
        4: "bot",
        5: "mid",
        6: "top",
        7: "bot",
        8: "supp",
        9: "jungle",
        10: "mid",
    }

    assert roles == roleml.predict(clean_game_na["game"], clean_game_na["game"]["timeline"])


def test_wrong_label():
    with pytest.raises(exceptions.WrongLabel):
        roleml.change_role_formatting("test")
