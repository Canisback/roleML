import os
import struct
import warnings

import joblib

from roleml.data.load_constants import constants
from roleml.exceptions import exceptions
from roleml.features import _get_features

_role_format = "clean"


def change_role_formatting(label_type: str):
    """Changes the role output formatting.

    Args:
        label_type: "clean", "rgapi", "full", "LolGame"
    """
    global _role_format
    if label_type not in ["clean", "rgapi", "full", "LolGame"]:
        raise exceptions.WrongLabel
    else:
        _role_format = label_type


def set_label_type(label_type):
    warnings.warn("change_role_formatting() should be used instead of set_label_type()", DeprecationWarning)
    change_role_formatting(label_type)


# Loading the model, ideally should be ghost loaded for faster package import
# 8 * struct.calcsize("P") == 32 tells is if the system is 32 or 64 bits
if 8 * struct.calcsize("P") == 32:
    model = joblib.load(os.path.join(os.path.dirname(__file__), "data", "role_identification_model_32bits.sav"))
else:
    model = joblib.load(os.path.join(os.path.dirname(__file__), "data", "role_identification_model_64bits.sav"))


def predict(match, timeline, cassiopeia_dicts=False) -> dict:
    """Predicts the role for all 10 players in the game.

    Args:
        match: a MatchDto
        timeline: the associated MatchTimelineDto
        cassiopeia_dicts: whether or not use cassiopeia feature names

    Returns:
        A dictionary mapping participantId to the role defined by _role_format
    """

    if match["gameDuration"] < 720:
        raise exceptions.MatchTooShort
    if not match["mapId"] == 11:
        raise exceptions.IncorrectMap

    df = _get_features(match, timeline, cassiopeia_dicts)

    df["role"] = model.predict(df.drop(["participantId"], axis=1))

    df = df.set_index(df["participantId"])

    participant_roles = df["role"].to_dict()

    if _role_format == "clean":
        return {k: constants["clean_roles"][participant_roles[k]] for k in participant_roles}
    elif _role_format == "rgapi":
        return {k: constants["riot_api_roles"][participant_roles[k]] for k in participant_roles}
    elif _role_format == "full":
        return {k: participant_roles[k] for k in participant_roles}
    elif _role_format == "LolGame":
        return {k: constants["LolGame"][participant_roles[k]] for k in participant_roles}
    else:
        raise exceptions.WrongLabel


def fix_game(match, timeline, fix_timeline=True):
    """Fixes a game by inserting the right roles.

    Args:
        match: a MatchDto
        timeline: the associated MatchTimelineDto
        fix_timeline: whether or not to iterate on the timeline to fix the "diff" fields

    Returns:
        match, timeline: the match and timeline with the predicted roles.

    Raises:
        NoOpponentFound if a player’s opponent could not be found
    """
    true_roles = predict(match, timeline)

    # Start by setting roles properly
    for participant in match["participants"]:
        participant["role"] = true_roles[participant["participantId"]]

    # Then, we iterate on the player’s timeline object and use its opponent to fill the right "diffs"
    if fix_timeline:
        for participant in match["participants"]:
            participant_id = participant["participantId"]

            possible_opponents = [
                opponent
                for opponent in match["participants"]
                if opponent["role"] == participant["role"] and opponent["participantId"] != participant["participantId"]
            ]

            if len(possible_opponents) != 1:
                raise exceptions.NoOpponentFoundException("Too many or too few opponents found.")

            opponent_id = possible_opponents[0]["participantId"]

            for frame in timeline["frames"]:
                frame = _fix_frame_keys(frame)
                participant_frame = frame["participantFrames"][str(participant_id)]
                opponent_frame = frame["participantFrames"][str(opponent_id)]

                participant_frame["totalGoldDiff"] = participant_frame["totalGold"] - opponent_frame["totalGold"]
                participant_frame["xpDiff"] = participant_frame["xp"] - opponent_frame["xp"]
                participant_frame["minionsKilledDiff"] = (
                    participant_frame["minionsKilled"] - opponent_frame["minionsKilled"]
                )
                participant_frame["jungleMinionsKilledDiff"] = (
                    participant_frame["jungleMinionsKilled"] - opponent_frame["jungleMinionsKilled"]
                )

    return match, timeline



def add_cass_predicted_roles(match):
    predicted_roles = predict(match.to_dict(), match.timeline.to_dict(), True)
    for p in match.participants:
        p.predicted_role = predicted_roles[p.id]


# Fixes participantFrames so that key is participantId
def _fix_frame_keys(frame):
    fixed_frame = {"participantFrames": {}, "events": frame["events"], "timestamp": frame["timestamp"]}
    for k, v in frame["participantFrames"].items():
        fixed_frame["participantFrames"][str(v["participantId"])] = v
    return fixed_frame


def fix_frame(frame):
    warnings.warn(
        "fix_frame() should likely be re-implemented in your own package and not imported.", DeprecationWarning
    )
    return _fix_frame_keys(frame)


def fix_and_augment_game_and_timeline(game, timeline, upgrade_participant=False, upgrade_timeline=False):
    warnings.warn(
        "fix_game() should be used instead and this function will disappear in a future version."
        "Its functionality is not supported anymore.", DeprecationWarning
    )

    return fix_game(game, timeline, fix_timeline=upgrade_timeline)
