import collections
import logging

import pandas as pd
import shapely.geometry

from roleml.data.load_constants import constants


def _get_features(match, timeline, cassiopeia_dicts=False):
    participants_features_list = []

    # Get the players positions form the timeline
    players_positions = _get_positions(timeline)

    players_most_frequent_lane = _get_most_frequent_lane(players_positions)
    players_lane_frequencies = _get_lane_frequencies(players_positions)

    if not cassiopeia_dicts:
        feature_names = {
            "participantId": "participantId",
            "spell1Id": "spell1Id",
            "spell2Id": "spell2Id",
            "minionsKilled": "minionsKilled",
            "jungleMinionsKilled": "jungleMinionsKilled",
        }
    else:
        feature_names = {
            "participantId": "id",
            "spell1Id": "summonerSpellDId",
            "spell2Id": "summonerSpellFId",
            "minionsKilled": "creepScore",
            "jungleMinionsKilled": "neutralMinionsKilled",
        }

    player_stats = _get_stats_at_10(timeline, feature_names)

    for participant in match["participants"]:

        participant_features = {}
        participant_id = participant[feature_names["participantId"]]

        lanes = ["jungle", "top", "mid", "bot"]

        # one hot encode positions
        for lane in lanes:
            participant_features["most-frequent-" + lane] = 0

        participant_features["most-frequent-" + players_most_frequent_lane[participant_id]] = 1

        # Lane frequency
        participant_features.update(
            {"lane-frequency-" + k: v for k, v in players_lane_frequencies[participant_id].items()}
        )

        # Init items lists
        for role in constants["role_composition"]:
            participant_features["has-item-overUsed-" + role] = 0
            participant_features["has-item-mostlyUsed-" + role] = 0
            participant_features["has-item-underUsed-" + role] = 0

        # Get the item ID for each of the 7 slots and check if they are in one of the three items lists
        for i in range(0, 7):
            # Check if there is an item for the slot
            if participant["stats"]["item" + str(i)] > 0:
                for role in constants["role_composition"]:

                    if str(participant["stats"]["item" + str(i)]) in constants["most_used_items"][role]:
                        participant_features["has-item-overUsed-" + role] = 1

                    if str(participant["stats"]["item" + str(i)]) in constants["decently_used_items"][role]:
                        participant_features["has-item-mostlyUsed-" + role] = 1

                    if str(participant["stats"]["item" + str(i)]) in constants["least_used_items"][role]:
                        participant_features["has-item-underUsed-" + role] = 1

        # Summoner spells
        participant_features.update(constants["spells"])
        if participant[feature_names["spell1Id"]] > 0:
            for feature_name in ("spell1Id", "spell2Id"):
                spell_name = "spell-{}".format(participant[feature_names[feature_name]])
                if spell_name in constants["spells"]:
                    participant_features[spell_name] = 1
                else:
                    # warning.warn is used for fixable warnings, logging.warning is recommended here
                    logging.warning(
                        "This game seems to be very old. "
                        "The model has never been tested for very old games, use with caution."
                    )

        # Player stats
        participant_features.update(player_stats[participant_id])

        participant_features["participantId"] = participant_id

        participants_features_list.append(participant_features)

    df = pd.DataFrame(participants_features_list)
    df = df.reindex(sorted(df.columns), axis=1)

    return df


def _get_positions(timeline: dict):
    """Computes the approximate lane position for the first 10 minutes of the game.
    """
    frames = timeline["frames"]

    participants_positions = collections.defaultdict(lambda: [])

    # We look at the snapshots from minute 1 to 10
    for i in range(1, 11):
        # For each participant
        for k in frames[i]["participantFrames"]:
            participant_id = frames[i]["participantFrames"][k]["participantId"]
            position = None

            # Position on the map
            coord = shapely.geometry.Point(
                frames[i]["participantFrames"][k]["position"]["x"], frames[i]["participantFrames"][k]["position"]["y"]
            )

            # Check where is the position
            if constants["jungle_blue"].contains(coord) or constants["jungle_red"].contains(coord):
                position = "jungle"
            elif constants["mid_lane"].contains(coord):
                position = "mid"
            elif constants["top_lane"].contains(coord):
                position = "top"
            elif constants["bot_lane"].contains(coord):
                position = "bot"
            # Save the position for the participant
            participants_positions[int(participant_id)].append(position)

    return participants_positions


def _get_most_frequent_lane(participants_positions):
    most_frequent_lane = {}
    for participant_id in participants_positions:
        lane_frequency = {'bot': 0, 'jungle': 0, 'mid': 0, 'top': 0}

        for lane in participants_positions[participant_id]:
            if lane is not None:
                lane_frequency[lane] += 1

        most_frequent_lane[participant_id] = max(lane_frequency, key=lane_frequency.get)

    return most_frequent_lane


def _get_lane_frequencies(participants_positions):
    lane_frequencies = {}
    for participant_id in participants_positions:
        lane_frequency = {"mid": 0, "top": 0, "bot": 0, "jungle": 0}

        for lane in participants_positions[participant_id]:
            if lane is not None:
                lane_frequency[lane] += 1

        lane_frequencies[participant_id] = lane_frequency

    return lane_frequencies


def _get_stats_at_10(timeline, feature_names=constants["feature_names"]):
    participant_frame = timeline["frames"][10]["participantFrames"]
    stats_at_10 = {}
    for k in participant_frame:
        participant_id = participant_frame[k]["participantId"]
        row = {
            "minionsKilled": participant_frame[k][feature_names["minionsKilled"]],
            "jungleMinionsKilled": participant_frame[k][feature_names["jungleMinionsKilled"]],
            "jungleMinionRatio": participant_frame[k][feature_names["jungleMinionsKilled"]]
            / (
                participant_frame[k][feature_names["minionsKilled"]]
                + participant_frame[k][feature_names["jungleMinionsKilled"]]
            )
            if participant_frame[k][feature_names["minionsKilled"]] > 0
            else 0,
        }
        stats_at_10[participant_id] = row

    return stats_at_10
