import joblib
import numpy as np
from shapely.geometry import Point, Polygon
import pandas as pd
import os
from sklearn.utils import _IS_32BIT

import warnings

from .utils import exceptions

# Initializing all the roles accepted
role_composition = {"JUNGLE_NONE", "TOP_SOLO", "MIDDLE_SOLO", "BOTTOM_DUO_CARRY", "BOTTOM_DUO_SUPPORT"}
clean_roles = {"JUNGLE_NONE": 'jungle', "TOP_SOLO": 'top', "MIDDLE_SOLO": 'mid',
               "BOTTOM_DUO_CARRY": 'bot', "BOTTOM_DUO_SUPPORT": 'supp'}
rgapi_roles = {
    "JUNGLE_NONE": {"lane":"JUNGLE","role":"NONE"}, 
    "TOP_SOLO": {"lane":"TOP","role":"SOLO"}, 
    "MIDDLE_SOLO": {"lane":"MIDDLE","role":"SOLO"},
    "BOTTOM_DUO_CARRY": {"lane":"BOTTOM","role":"DUO_CARRY"}, 
    "BOTTOM_DUO_SUPPORT": {"lane":"BOTTOM","role":"DUO_SUPPORT"}
}

# Init spells
spells = {'spell-21': 0, 'spell-1': 0, 'spell-14': 0, 'spell-3': 0, 'spell-4': 0, 'spell-6': 0, 'spell-7': 0,
          'spell-11': 0, 'spell-12': 0}

# Static data for lane position
midlane = Polygon(
    [(4200, 3500), (11300, 10500), (13200, 13200), (10500, 11300), (3300, 4400), (1600, 1600)])
toplane = Polygon(
    [(-120, 1600), (-120, 14980), (13200, 14980), (13200, 13200), (4000, 13200), (1600, 11000), (1600, 1600)])
botlane = Polygon(
    [(1600, -120), (14870, -120), (14870, 13200), (13200, 13200), (13270, 4000), (10500, 1700), (1600, 1600)])
jungle1 = Polygon(
    [(1600, 5000), (1600, 11000), (4000, 13200), (9800, 13200), (10500, 11300), (3300, 4400)])
jungle2 = Polygon(
    [(5000, 1700), (4200, 3500), (11300, 10500), (13270, 9900), (13270, 4000), (10500, 1700)])

# Init features_name
feature_names = {'participantId': 'participantId', 'spell1Id': 'spell1Id', 'spell2Id': 'spell2Id',
                         'minionsKilled': 'minionsKilled', 'jungleMinionsKilled': 'jungleMinionsKilled'}

# Static data for item frequency
overUsedItems = {
    'BOTTOM_DUO_SUPPORT': ['3050', '3069', '3092', '3096', '3097', '3098', '3105', '3107', '3114', '3222', '3382',
                           '3401', '3504', '3850', '3851', '3853', '3854', '3855', '3857', '3858', '3859', '3860',
                           '3862', '3863', '3864'],
    'JUNGLE_NONE': ['1039', '1041', '1400', '1401', '1402', '1412', '1413', '1414', '1416', '1419', '2057', '3706',
                    '3715'],
    'TOP_SOLO': ['3068', '3161', '3196', '3373', '3379'],
    'BOTTOM_DUO_CARRY': ['2319', '3004', '3042', '3095', '3389'],
    'MIDDLE_SOLO': ['3197']
}
mostlyUsedItems = {
    'BOTTOM_DUO_SUPPORT': ['1004', '2065', '2403', '3024', '3028', '3109', '3117', '3174', '3190', '3383', '3801'],
    'JUNGLE_NONE': ['3083', '3380', '3513'],
    'TOP_SOLO': ['2053', '3022', '3056', '3074', '3387', '3512', '3748', '3751', '3812'],
    'BOTTOM_DUO_CARRY': ['1042', '1043', '1051', '1055', '1083', '2011', '2015', '2060', '2061', '3006', '3025', '3031',
                         '3046', '3072', '3085', '3086', '3087', '3094', '3124', '3139', '3140', '3144', '3153', '3363',
                         '3371', '3508'],
    'MIDDLE_SOLO': ['1056', '3003', '3027', '3030', '3040', '3198', '3285', '3390']
}

underUsedItems = {
    'BOTTOM_DUO_SUPPORT': ['1011', '1018', '1036', '1037', '1038', '1039', '1041', '1042', '1043', '1051', '1053',
                           '1054', '1055', '1056', '1057', '1058', '1083', '1400', '1401', '1402', '1412', '1413',
                           '1414', '1416', '1419', '2011', '2015', '2033', '2057', '2058', '2059', '2061', '2062',
                           '2140', '2319', '2420', '2421', '3001', '3004', '3006', '3020', '3022', '3025', '3026',
                           '3027', '3031', '3033', '3035', '3036', '3040', '3042', '3044', '3046', '3047', '3052',
                           '3053', '3057', '3065', '3068', '3071', '3072', '3074', '3075', '3076', '3077', '3078',
                           '3083', '3085', '3086', '3087', '3089', '3091', '3094', '3095', '3100', '3101', '3102',
                           '3115', '3123', '3124', '3135', '3139', '3140', '3142', '3143', '3144', '3146', '3152',
                           '3153', '3155', '3156', '3161', '3165', '3193', '3194', '3196', '3197', '3198', '3211',
                           '3285', '3340', '3363', '3371', '3373', '3374', '3379', '3380', '3384', '3386', '3387',
                           '3389', '3508', '3513', '3706', '3715', '3742', '3748', '3751', '3812', '3814', '3907',
                           '3916'],
    'JUNGLE_NONE': ['1004', '1006', '1018', '1051', '1053', '1054', '1055', '1056', '1083', '2003', '2004', '2010',
                    '2011', '2013', '2015', '2033', '2053', '2056', '2058', '2059', '2060', '2061', '2062', '2065',
                    '2319', '2403', '2422', '2423', '2424', '3003', '3004', '3006', '3009', '3024', '3025', '3027',
                    '3028', '3030', '3031', '3040', '3042', '3046', '3050', '3056', '3068', '3069', '3070', '3072',
                    '3086', '3087', '3092', '3094', '3095', '3096', '3097', '3098', '3105', '3107', '3114', '3115',
                    '3116', '3123', '3124', '3139', '3140', '3146', '3152', '3153', '3158', '3161', '3190', '3196',
                    '3197', '3198', '3222', '3285', '3301', '3302', '3363', '3371', '3373', '3379', '3382', '3389',
                    '3390', '3401', '3504', '3508', '3751', '3801', '3802', '3812', '3905', '3907'],
    'TOP_SOLO': ['1004', '1039', '1041', '1042', '1051', '1400', '1401', '1402', '1412', '1413', '1414', '1416', '1419',
                 '2003', '2015', '2055', '2057', '2065', '2319', '2423', '3004', '3006', '3009', '3028', '3031', '3041',
                 '3042', '3046', '3050', '3069', '3072', '3085', '3086', '3092', '3094', '3095', '3096', '3097', '3098',
                 '3100', '3105', '3107', '3109', '3113', '3114', '3117', '3124', '3139', '3145', '3153', '3158', '3174',
                 '3190', '3197', '3222', '3285', '3303', '3363', '3364', '3371', '3374', '3380', '3382', '3386', '3388',
                 '3389', '3390', '3401', '3504', '3513', '3706', '3715', '3801', '3905'],
    'BOTTOM_DUO_CARRY': ['1001', '1004', '1006', '1011', '1026', '1027', '1028', '1029', '1031', '1039', '1041', '1052',
                         '1056', '1058', '1082', '1400', '1401', '1402', '1412', '1413', '1414', '1416', '1419', '2033',
                         '2053', '2055', '2057', '2065', '2138', '2139', '2403', '3001', '3003', '3010', '3020', '3024',
                         '3027', '3028', '3030', '3040', '3041', '3044', '3047', '3050', '3052', '3053', '3056', '3057',
                         '3065', '3067', '3068', '3069', '3070', '3071', '3074', '3075', '3076', '3077', '3078', '3082',
                         '3083', '3089', '3092', '3096', '3097', '3098', '3100', '3102', '3105', '3107', '3108', '3109',
                         '3110', '3111', '3113', '3114', '3116', '3117', '3134', '3135', '3136', '3142', '3143', '3147',
                         '3151', '3152', '3157', '3161', '3165', '3174', '3190', '3191', '3193', '3194', '3196', '3197',
                         '3198', '3211', '3222', '3285', '3303', '3340', '3364', '3373', '3374', '3379', '3380', '3382',
                         '3383', '3387', '3390', '3401', '3504', '3512', '3513', '3706', '3715', '3742', '3748', '3751',
                         '3800', '3801', '3812', '3814', '3905', '3907', '3916'],
    'MIDDLE_SOLO': ['1004', '1006', '1011', '1029', '1031', '1033', '1039', '1041', '1042', '1043', '1051', '1055',
                    '1057', '1083', '1400', '1401', '1402', '1412', '1413', '1414', '1416', '1419', '2010', '2011',
                    '2013', '2015', '2053', '2056', '2057', '2058', '2060', '2061', '2062', '2065', '2138', '2140',
                    '2319', '3004', '3006', '3009', '3010', '3022', '3024', '3025', '3028', '3042', '3046', '3047',
                    '3050', '3056', '3065', '3067', '3068', '3069', '3071', '3072', '3074', '3075', '3076', '3082',
                    '3083', '3085', '3086', '3092', '3094', '3095', '3096', '3097', '3098', '3101', '3105', '3107',
                    '3109', '3110', '3114', '3117', '3123', '3124', '3139', '3143', '3144', '3153', '3161', '3174',
                    '3190', '3193', '3194', '3196', '3211', '3222', '3301', '3364', '3373', '3379', '3382', '3383',
                    '3387', '3389', '3401', '3504', '3508', '3512', '3513', '3706', '3715', '3742', '3751', '3800',
                    '3801']
}

# TODO : these should not be static
#       Need to set up an external resource to call for item frequencies for the current patch.
#       Even better would be for each patch.


_label_type = "clean"

def set_label_type(label_type):
    global _label_type
    if not label_type in ["clean","rgapi","full"]:
        raise exceptions.WrongLabel
    else:
        _label_type = label_type

# Loading the model
if _IS_32BIT:
    roleml_model = joblib.load(os.path.join(os.path.dirname(__file__), "role_identification_model_32bits.sav"))
else:
    roleml_model = joblib.load(os.path.join(os.path.dirname(__file__), "role_identification_model_64bits.sav"))


def get_positions(timeline):
    frames = timeline['frames']

    participants_positions = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
    # 10 first frames except the really first one, when everybody spawn
    for i in range(1, 11):
        # For each participant
        for k in frames[i]['participantFrames']:
            participantId = frames[i]['participantFrames'][k]["participantId"]
            position = None

            # Position on the map
            coord = Point(frames[i]['participantFrames'][k]['position']['x'],
                     frames[i]['participantFrames'][k]['position']['y'])
            # Check where is the position
            if jungle1.contains(coord) or jungle2.contains(coord):
                position = "jungle"
            elif midlane.contains(coord):
                position = "mid"
            elif toplane.contains(coord):
                position = "top"
            elif botlane.contains(coord):
                position = "bot"
            # Save the position for the participant
            participants_positions[int(participantId)].append(position)

    return participants_positions


def get_most_frequent_lane(participants_positions):
    most_frequent_lane = {}
    for participant_id in participants_positions:
        lane_frequency = {"mid": 0, "top": 0, "bot": 0, "jungle": 0}

        for lane in participants_positions[participant_id]:
            if lane is not None:
                lane_frequency[lane] += 1

        most_frequent_lane[participant_id] = max(lane_frequency, key=lane_frequency.get)

    return most_frequent_lane


def get_lane_frequencies(participants_positions):
    lane_frequencies = {}
    for participant_id in participants_positions:
        lane_frequency = {"mid": 0, "top": 0, "bot": 0, "jungle": 0}

        for lane in participants_positions[participant_id]:
            if lane is not None:
                lane_frequency[lane] += 1

        lane_frequencies[participant_id] = lane_frequency

    return lane_frequencies


def get_stats_at_10(timeline, feature_names=feature_names):
    participant_frame = timeline['frames'][10]['participantFrames']
    stats_at_10 = {}
    for k in participant_frame:
        participantId = participant_frame[k]["participantId"]
        row = {
            "minionsKilled": participant_frame[k][feature_names["minionsKilled"]],
            "jungleMinionsKilled": participant_frame[k][feature_names["jungleMinionsKilled"]],
            "jungleMinionRatio": participant_frame[k][feature_names["jungleMinionsKilled"]] /
                                 (participant_frame[k][feature_names["minionsKilled"]] + participant_frame[k][
                                     feature_names["jungleMinionsKilled"]])
            if participant_frame[k][feature_names["minionsKilled"]] > 0 else 0
        }
        stats_at_10[participantId] = row

    return stats_at_10


def get_features(match, timeline, cassiopeia_dicts = False):
    participants_features_list = []

    # Get the players positions form the timeline
    players_positions = get_positions(timeline)

    player_most_frequent_lane = get_most_frequent_lane(players_positions)
    player_lane_frequencies = get_lane_frequencies(players_positions)

    if not cassiopeia_dicts:
        feature_names = {'participantId': 'participantId', 'spell1Id': 'spell1Id', 'spell2Id': 'spell2Id',
                         'minionsKilled': 'minionsKilled', 'jungleMinionsKilled': 'jungleMinionsKilled'}
    else:
        feature_names = {'participantId': 'id', 'spell1Id': 'summonerSpellDId', 'spell2Id': 'summonerSpellFId',
                         'minionsKilled': 'creepScore', 'jungleMinionsKilled': 'neutralMinionsKilled'}

    player_stats = get_stats_at_10(timeline, feature_names)

    for participant in match['participants']:

        participant_features = {}

        participant_id = participant[feature_names["participantId"]]

        lanes = ["jungle", "top", "mid", "bot"]

        # one hot encode positions
        for lane in lanes:
            participant_features['most-frequent-' + lane] = 0

        participant_features['most-frequent-' + player_most_frequent_lane[participant_id]] = 1

        # Lane frequency
        participant_features.update({"lane-frequency-" + k: v for k, v in
                                     player_lane_frequencies[participant_id].items()})

        # Init items lists
        for role in role_composition:
            participant_features["has-item-overUsed-" + role] = 0
            participant_features["has-item-mostlyUsed-" + role] = 0
            participant_features["has-item-underUsed-" + role] = 0

        # Get the item ID for each of the 7 slots and check if they are in one of the three items lists
        for i in range(0, 7):
            # Check if there is an item for the slot
            if participant['stats']['item' + str(i)] > 0:
                for role in role_composition:

                    if str(participant['stats']['item' + str(i)]) in overUsedItems[role]:
                        participant_features["has-item-overUsed-" + role] = 1

                    if str(participant['stats']['item' + str(i)]) in mostlyUsedItems[role]:
                        participant_features["has-item-mostlyUsed-" + role] = 1

                    if str(participant['stats']['item' + str(i)]) in underUsedItems[role]:
                        participant_features["has-item-underUsed-" + role] = 1

        # Summoner spells
        participant_features.update(spells)
        if participant[feature_names["spell1Id"]] > 0:
            for feature_name in ("spell1Id", "spell2Id"):
                spell_name = "spell-{}".format(participant[feature_names[feature_name]])
                if spell_name in spells:
                    participant_features[spell_name] = 1
                else:
                    warnings.warn("This game seems to be very old. The model has never been tested for very old games, use with caution.")

        # Player stats
        participant_features.update(player_stats[participant_id])

        participant_features["participantId"] = participant_id

        participants_features_list.append(participant_features)

    df = pd.DataFrame(participants_features_list)

    df = df.reindex(sorted(df.columns), axis=1)

    return df


def predict(match, timeline, cassiopeia_dicts=False):
    if match["gameDuration"] < 720:
        raise exceptions.MatchTooShort
    if not match["mapId"] == 11:
        raise exceptions.IncorrectMap

    df = get_features(match, timeline, cassiopeia_dicts)

    df["role"] = roleml_model.predict(df.drop(["participantId"], axis=1))

    df = df.set_index(df["participantId"])

    participant_roles = df["role"].to_dict()
    
    print(_label_type)
    if _label_type == "clean":
        return {k: clean_roles[participant_roles[k]] for k in participant_roles}
    elif _label_type == "rgapi":
        return {k: rgapi_roles[participant_roles[k]] for k in participant_roles}
    elif _label_type == "full":
        return {k: participant_roles[k] for k in participant_roles}
    else:
        raise Exception("Don't mess with the label")
        
        


# Fixes participantFrames so that key is participantId
def fix_frame(frame):
    fixed_frame = {"participantFrames": {}, 'events': frame["events"], 'timestamp': frame["timestamp"]}
    for k, v in frame["participantFrames"].items():
        fixed_frame["participantFrames"][str(v["participantId"])] = v
    return fixed_frame


def fix_and_augment_game_and_timeline(game, timeline, upgrade_participant=False, upgrade_timeline=False):
    true_roles = predict(game, timeline)

    # First, set all roles properly so we know player's opponents
    for participant in game['participants']:
        participant['role'] = true_roles[participant['participantId']]

    # Second, add the diffs in the frames. We're not using the "deltas" since it's redundant info
    for participant in game['participants']:
        participant_id = participant['participantId']

        opponent_found = None
        for opponent in game['participants']:
            opponent_id = opponent['participantId']
            if opponent_id != participant_id and opponent['role'] == participant['role']:
                opponent_found = True
                break

        if opponent_found is None:
            raise Exception('Player without opponent found')

        if not game['participants'][opponent_id - 1]['participantId'] == opponent_id:
            raise Exception('Opponent array detection screwed')

        participant_timeline = participant['timeline']
        opponent_timeline = game['participants'][opponent_id - 1]['timeline']

        # Reseting or creating stats per min fields
        participant_timeline['csDiffPerMinDeltas'] = {}
        for i in participant_timeline['creepsPerMinDeltas']:
            participant_timeline['csDiffPerMinDeltas'][i] = round(
                participant_timeline['creepsPerMinDeltas'][i] - opponent_timeline['creepsPerMinDeltas'][i], 2)

        participant_timeline['xpDiffPerMinDeltas'] = {}
        for i in participant_timeline['xpPerMinDeltas']:
            participant_timeline['xpDiffPerMinDeltas'][i] = round(
                participant_timeline['xpPerMinDeltas'][i] - opponent_timeline['xpPerMinDeltas'][i], 2)

        participant_timeline['damageTakenDiffPerMinDeltas'] = {}
        for i in participant_timeline['damageTakenPerMinDeltas']:
            participant_timeline['damageTakenDiffPerMinDeltas'][i] = round(
                participant_timeline['damageTakenPerMinDeltas'][i] - opponent_timeline['damageTakenPerMinDeltas'][i], 2)

        if upgrade_participant:
            participant_timeline['goldDiffPerMinDeltas'] = {}
            for i in participant_timeline['goldPerMinDeltas']:
                participant_timeline['goldDiffPerMinDeltas'][i] = round(
                    participant_timeline['goldPerMinDeltas'][i] - opponent_timeline['goldPerMinDeltas'][i], 2)

        if upgrade_timeline:
            for frame in timeline['frames']:
                frame = fix_frame(frame)
                participant_frame = frame['participantFrames'][str(participant_id)]
                opponent_frame = frame['participantFrames'][str(opponent_id)]

                participant_frame['totalGoldDiff'] = participant_frame['totalGold'] - opponent_frame['totalGold']
                participant_frame['xpDiff'] = participant_frame['xp'] - opponent_frame['xp']
                participant_frame['minionsKilledDiff'] = \
                    participant_frame['minionsKilled'] - opponent_frame['minionsKilled']
                participant_frame['jungleMinionsKilledDiff'] = \
                    participant_frame['jungleMinionsKilled'] - opponent_frame['jungleMinionsKilled']

    if not upgrade_participant:
        for participant in game['participants']:
            del (participant['role'])

    return game, timeline

def add_cass_predicited_roles(match):
    predicted_roles = predict(match.to_dict(), match.timeline.to_dict(), True)
    for p in match.participants:
        p.predicted_role = predicted_roles[p.id]