import json
import os
from typing import TypedDict, Dict

import pytest


class TestGame(TypedDict, total=False):
    game: dict
    expected_roles: Dict[int, str]
    stats_at_10: Dict
    participants_positions: Dict
    lane_frequency: Dict
    most_frequent_lane: Dict


@pytest.fixture
def clean_game_na():
    with open(os.path.join(os.path.dirname(__file__), "data", "NA-3023745286.json"), "r") as f:
        game = json.load(f)

    return TestGame(
        game=game,
        expected_roles={
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
        },
        stats_at_10={
            1: {"minionsKilled": 2, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            2: {"minionsKilled": 7, "jungleMinionsKilled": 44, "jungleMinionRatio": 0.8627450980392157},
            3: {"minionsKilled": 49, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            4: {"minionsKilled": 50, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            5: {"minionsKilled": 34, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            6: {"minionsKilled": 56, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            7: {"minionsKilled": 47, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            8: {"minionsKilled": 12, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            9: {"minionsKilled": 1, "jungleMinionsKilled": 35, "jungleMinionRatio": 0.9722222222222222},
            10: {"minionsKilled": 58, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
        },
        participants_positions={
            1: ["jungle", "bot", "bot", "bot", "bot", "bot", "jungle", "bot", "bot", "bot"],
            2: ["jungle", "jungle", "jungle", "jungle", "bot", "jungle", None, "jungle", "jungle", "top"],
            3: ["top", "top", "jungle", "top", "top", "top", "top", "top", "top", "top"],
            4: [None, "bot", "bot", "bot", "bot", "bot", "bot", "bot", "bot", "bot"],
            5: [None, "mid", "jungle", "mid", None, "mid", "mid", "mid", None, "mid"],
            6: ["top", "top", "top", "jungle", "top", "top", "top", "jungle", "top", "top"],
            7: ["jungle", "bot", "bot", "bot", None, "bot", "bot", "bot", "bot", "bot"],
            8: ["jungle", "bot", "bot", "bot", "bot", "bot", None, "bot", "bot", "bot"],
            9: ["jungle", "jungle", "jungle", "jungle", "jungle", "jungle", "jungle", "top", "jungle", "jungle"],
            10: ["jungle", "mid", "mid", "mid", "mid", "mid", "mid", "mid", None, "mid"],
        },
        lane_frequency={
            1: {"bot": 8, "jungle": 2, "mid": 0, "top": 0},
            2: {"jungle": 7, "bot": 1, "top": 1, "mid": 0},
            3: {"top": 9, "jungle": 1, "mid": 0, "bot": 0},
            4: {"bot": 9, "jungle": 0, "mid": 0, "top": 0},
            5: {"mid": 6, "jungle": 1, "top": 0, "bot": 0},
            6: {"top": 8, "jungle": 2, "mid": 0, "bot": 0},
            7: {"bot": 8, "jungle": 1, "mid": 0, "top": 0},
            8: {"bot": 8, "jungle": 1, "mid": 0, "top": 0},
            9: {"jungle": 9, "top": 1, "bot": 0, "mid": 0},
            10: {"mid": 8, "jungle": 1, "top": 0, "bot": 0},
        },
        most_frequent_lane={
            1: "bot",
            2: "jungle",
            3: "top",
            4: "bot",
            5: "mid",
            6: "top",
            7: "bot",
            8: "bot",
            9: "jungle",
            10: "mid",
        },
    )


@pytest.fixture
def clean_game_euw():
    with open(os.path.join(os.path.dirname(__file__), "data", "EUW-3692606327.json"), "r") as f:
        game = json.load(f)

    return TestGame(
        game=game,
        expected_roles={
            1: "supp",
            2: "top",
            3: "mid",
            4: "jungle",
            5: "bot",
            6: "top",
            7: "supp",
            8: "mid",
            9: "jungle",
            10: "bot",
        },
        stats_at_10={
            1: {"minionsKilled": 3, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            2: {"minionsKilled": 63, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            3: {"minionsKilled": 59, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            4: {"minionsKilled": 12, "jungleMinionsKilled": 44, "jungleMinionRatio": 0.7857142857142857},
            5: {"minionsKilled": 78, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            6: {"minionsKilled": 70, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            7: {"minionsKilled": 11, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            8: {"minionsKilled": 48, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
            9: {"minionsKilled": 1, "jungleMinionsKilled": 40, "jungleMinionRatio": 0.975609756097561},
            10: {"minionsKilled": 46, "jungleMinionsKilled": 0, "jungleMinionRatio": 0.0},
        },
    )


@pytest.fixture
def short_game():
    with open(os.path.join(os.path.dirname(__file__), "data", "EUW-4236896092.json"), "r") as f:
        game = json.load(f)

    return TestGame(game=game)


@pytest.fixture
def aram_game():
    with open(os.path.join(os.path.dirname(__file__), "data", "EUW-4458819927.json"), "r") as f:
        game = json.load(f)

    return TestGame(game=game)


@pytest.fixture
def pro_game():
    with open(os.path.join(os.path.dirname(__file__), "data", "TR1-266041574.json"), "r") as f:
        game = json.load(f)

    return TestGame(game=game)


@pytest.fixture
def opponent_not_found_game():
    with open(os.path.join(os.path.dirname(__file__), "data", "EUW-4233525244.json"), "r") as f:
        data = json.load(f)

    return TestGame(game=data)

@pytest.fixture
def empty_lane_frequency_game():
    with open(os.path.join(os.path.dirname(__file__), "data", "EUW-4664197701.json"), "r") as f:
        data = json.load(f)

    return TestGame(game=data)
