from sklearn.externals import joblib
import numpy as np
import matplotlib.path as mplPath
import pandas as pd

#Initializing all the roles accepted
role_composition = set(["JUNGLE_NONE","TOP_SOLO","MIDDLE_SOLO","BOTTOM_DUO_CARRY","BOTTOM_DUO_SUPPORT"])

#Init spells
spells = {'spell-21': 0,'spell-1': 0,'spell-14': 0,'spell-3': 0,'spell-4': 0,'spell-6': 0,'spell-7': 0,'spell-11': 0,'spell-12': 0}

#Static data for lane position
midlane = mplPath.Path(np.array([[4200 ,3500],[11300 ,10500],[13200 ,13200],[10500 ,11300],[3300 ,4400],[1600,1600]]))
toplane = mplPath.Path(np.array([[-120 ,1600],[-120 ,14980],[13200 ,14980],[13200 ,13200],[4000 ,13200],[1600,11000],[1600 ,1600]]))
botlane = mplPath.Path(np.array([[1600 ,-120],[14870,-120],[14870,13200],[13200,13200],[13270,4000],[10500,1700],[1600,1600]]))
jungle1 = mplPath.Path(np.array([[1600,5000],[1600,11000],[4000 ,13200],[9800 ,13200],[10500 ,11300],[3300 ,4400]]))
jungle2 = mplPath.Path(np.array([[5000,1700],[4200 ,3500],[11300 ,10500],[13270,9900],[13270,4000],[10500,1700]]))

#Static data for item frequency
overUsedItems = {"BOTTOM_DUO_SUPPORT": ["3028", "3050", "3069", "3092", "3096", "3097", "3098", "3105", "3107", "3114", "3222", "3303", "3382", "3401", "3504", "3600"], "JUNGLE_NONE": ["1039", "1041", "1400", "1401", "1402", "1412", "1413", "1414", "1416", "1419", "2032", "3706", "3715"], "TOP_SOLO": ["3068", "3196", "3373", "3379"], "BOTTOM_DUO_CARRY": ["3004", "3042", "3085", "3094", "3124", "3153", "3389"], "MIDDLE_SOLO": []}
mostlyUsedItems = {"BOTTOM_DUO_SUPPORT": ["1004", "2065", "2403", "3109", "3117", "3174", "3190", "3383", "3801", "3905"], "JUNGLE_NONE": ["3083", "3513", "3742"], "TOP_SOLO": ["2053", "3001", "3056", "3074", "3075", "3076", "3110", "3194", "3197", "3387", "3508", "3512", "3748", "3751", "3800", "3812"], "BOTTOM_DUO_CARRY": ["1042", "1043", "1051", "1055", "1083", "2004", "2011", "2013", "2015", "2056", "2057", "2058", "2059", "2060", "2061", "2062", "2319", "3003", "3006", "3025", "3031", "3072", "3086", "3087", "3095", "3139", "3140", "3144", "3363", "3371"], "MIDDLE_SOLO": ["1056", "1058", "3027", "3089", "3102", "3285", "3374", "3390"]}
underUsedItems = {"BOTTOM_DUO_SUPPORT": ["1011", "1036", "1037", "1038", "1039", "1041", "1042", "1043", "1051", "1053", "1054", "1055", "1056", "1058", "1083", "1400", "1401", "1402", "1412", "1413", "1414", "1416", "1419", "2004", "2011", "2013", "2015", "2032", "2033", "2056", "2057", "2058", "2059", "2060", "2061", "2062", "2140", "2319", "2420", "3001", "3003", "3004", "3006", "3022", "3025", "3026", "3027", "3031", "3033", "3035", "3036", "3040", "3042", "3044", "3046", "3047", "3052", "3053", "3056", "3057", "3065", "3068", "3071", "3072", "3074", "3075", "3076", "3077", "3078", "3083", "3085", "3086", "3087", "3089", "3091", "3094", "3095", "3100", "3101", "3102", "3111", "3115", "3123", "3124", "3135", "3139", "3140", "3142", "3143", "3144", "3145", "3146", "3152", "3153", "3155", "3156", "3165", "3193", "3194", "3196", "3197", "3198", "3211", "3285", "3301", "3340", "3363", "3371", "3373", "3374", "3379", "3380", "3384", "3387", "3388", "3389", "3508", "3512", "3513", "3520", "3706", "3715", "3742", "3748", "3751", "3812", "3814", "3907"], "JUNGLE_NONE": ["1004", "1043", "1051", "1053", "1054", "1055", "1056", "1058", "1083", "2003", "2004", "2010", "2011", "2013", "2015", "2033", "2056", "2057", "2058", "2059", "2060", "2061", "2062", "2065", "2139", "2319", "2403", "2422", "2423", "3003", "3004", "3006", "3009", "3025", "3027", "3028", "3030", "3031", "3040", "3042", "3046", "3050", "3056", "3068", "3069", "3070", "3072", "3085", "3086", "3087", "3092", "3094", "3095", "3096", "3097", "3098", "3105", "3107", "3108", "3114", "3115", "3116", "3123", "3124", "3139", "3140", "3144", "3146", "3151", "3152", "3153", "3158", "3190", "3196", "3197", "3198", "3222", "3285", "3301", "3302", "3303", "3363", "3371", "3373", "3379", "3382", "3383", "3387", "3389", "3390", "3401", "3504", "3508", "3600", "3751", "3801", "3802", "3905", "3907"], "TOP_SOLO": ["1004", "1039", "1041", "1042", "1043", "1051", "1400", "1401", "1402", "1412", "1413", "1414", "1416", "1419", "2003", "2015", "2032", "2055", "2065", "2140", "2423", "3003", "3004", "3006", "3009", "3028", "3030", "3031", "3041", "3042", "3050", "3069", "3070", "3072", "3085", "3086", "3092", "3094", "3095", "3096", "3097", "3098", "3100", "3105", "3107", "3109", "3114", "3117", "3124", "3144", "3153", "3174", "3190", "3222", "3285", "3302", "3303", "3363", "3364", "3371", "3374", "3380", "3382", "3386", "3388", "3389", "3390", "3401", "3504", "3600", "3706", "3715", "3802", "3905"], "BOTTOM_DUO_CARRY": ["1004", "1006", "1011", "1026", "1028", "1029", "1031", "1039", "1041", "1052", "1057", "1058", "1082", "1400", "1401", "1402", "1412", "1413", "1414", "1416", "1419", "2032", "2033", "2053", "2055", "2065", "2138", "2403", "2423", "2424", "3001", "3010", "3020", "3024", "3027", "3028", "3041", "3050", "3052", "3053", "3056", "3057", "3065", "3067", "3068", "3069", "3074", "3075", "3076", "3077", "3078", "3082", "3083", "3089", "3092", "3096", "3097", "3098", "3100", "3102", "3105", "3107", "3108", "3109", "3110", "3111", "3113", "3114", "3117", "3134", "3135", "3136", "3142", "3143", "3147", "3151", "3152", "3157", "3165", "3174", "3190", "3191", "3193", "3194", "3196", "3197", "3198", "3211", "3222", "3285", "3301", "3303", "3340", "3364", "3373", "3374", "3379", "3382", "3383", "3384", "3386", "3387", "3388", "3390", "3401", "3504", "3512", "3520", "3600", "3706", "3715", "3742", "3748", "3751", "3800", "3801", "3812", "3814", "3905", "3907", "3916"], "MIDDLE_SOLO": ["1004", "1006", "1011", "1029", "1031", "1033", "1038", "1039", "1041", "1042", "1043", "1051", "1057", "1083", "1400", "1401", "1402", "1412", "1413", "1414", "1416", "1419", "2004", "2010", "2011", "2013", "2015", "2032", "2053", "2055", "2056", "2057", "2058", "2059", "2060", "2061", "2062", "2065", "2138", "2319", "2422", "3001", "3004", "3006", "3009", "3010", "3024", "3025", "3026", "3028", "3042", "3044", "3047", "3050", "3056", "3065", "3067", "3068", "3069", "3071", "3072", "3074", "3075", "3076", "3078", "3082", "3083", "3085", "3086", "3087", "3092", "3094", "3095", "3096", "3097", "3098", "3101", "3105", "3107", "3109", "3110", "3114", "3117", "3123", "3124", "3133", "3139", "3143", "3144", "3153", "3156", "3174", "3190", "3193", "3194", "3196", "3211", "3222", "3303", "3364", "3373", "3379", "3382", "3383", "3387", "3389", "3401", "3504", "3508", "3512", "3513", "3600", "3706", "3715", "3742", "3748", "3751", "3800", "3801", "3812"]}
#TODO : these should not be static
#       Need to set up an external resource to call for item frequencies for the current patch. Even better would be for each patch.




#Loading the model
roleml_model = joblib.load("role_identification_model.sav")


def getPositions(timeline):
    frames = timeline['frames']
    
    participantsPositions = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[]}
    # 10 first frames except the really first one, when everybody spawn
    for i in range(1,11):
        # For each participant
        for k in frames[i]['participantFrames']:
            position = None
            
            # Position on the map
            coord = [frames[i]['participantFrames'][k]['position']['x'],frames[i]['participantFrames'][k]['position']['y']]
            # Check where is the position
            if jungle1.contains_point(coord) or jungle2.contains_point(coord):
                position = "jungle"
            elif midlane.contains_point(coord):
                position = "mid"
            elif toplane.contains_point(coord):
                position = "top"
            elif botlane.contains_point(coord):
                position = "bot"
            # Save the position for the participant
            participantsPositions[int(k)].append(position)
    return participantsPositions

def getMostFrequentLane(participantsPositions):
    mostFrequentLane = {}
    for participant in participantsPositions:
        laneFrequency = {"mid":0,"top":0,"bot":0,"jungle":0}
        
        for lane in participantsPositions[participant]:
            if not lane == None:
                laneFrequency[lane] += 1
        
        mostFrequentLane[participant] = max(laneFrequency, key=laneFrequency.get)
    return mostFrequentLane

def getLaneFrequencies(participantsPositions):
    laneFrequencies = {}
    for participant in participantsPositions:
        laneFrequency = {"mid":0,"top":0,"bot":0,"jungle":0}
        
        for lane in participantsPositions[participant]:
            if not lane == None:
                laneFrequency[lane] += 1
        
        laneFrequencies[participant] = laneFrequency
    return laneFrequencies


def getStatsAt10(timeline):
    participantFrame = timeline['frames'][10]['participantFrames']
    
    p = {}
    for k in participantFrame:
        row = {
            "minionsKilled":participantFrame[k]["minionsKilled"],
            "jungleMinionsKilled":participantFrame[k]["jungleMinionsKilled"],
            "jungleMinionRatio":participantFrame[k]["jungleMinionsKilled"]/(participantFrame[k]["minionsKilled"]+participantFrame[k]["jungleMinionsKilled"]) if participantFrame[k]["minionsKilled"] > 0 else 0
        }
        p[k] = row
    return p

def predict(match, timeline):
    
    if match["gameDuration"] < 720:
        raise Exception("Match too short")
    
    participantRoles = {}
    participantList = []
    
    #Get the players positions form the timeline
    playersPositions = getPositions(timeline)
    
    playerMostFrequentLane = getMostFrequentLane(playersPositions)
    playerLaneFrequencies = getLaneFrequencies(playersPositions)
    
    playerStats = getStatsAt10(timeline)
    
    for p in match['participants']:
            
        participant = {}
        
        participantId = p["participantId"]
        
        lanes = ["jungle","top","mid","bot"]
        
        #one hot encode positions
        for lane in lanes:
            participant['most-frequent-'+lane] = 0
        
        participant['most-frequent-'+ playerMostFrequentLane[participantId]] = 1
        
        #Lane frequency
        participant = {**participant, **{"lane-frequency-"+k:v for k,v in playerLaneFrequencies[participantId].items()} }
        
                
        #Init items lists 
        for role in role_composition:
            participant["has-item-overUsed-"+role] = 0
            participant["has-item-mostlyUsed-"+role] = 0
            participant["has-item-underUsed-"+role] = 0
        
        #Get the item ID for each of the 7 slots and check if they are in one of the three items lists
        for i in range(0,7):
            
            #Check if there is an item for the slot
            if p['stats']['item'+str(i)] > 0:
                for role in role_composition:

                    if str(p['stats']['item'+str(i)]) in overUsedItems[role]:
                        participant["has-item-overUsed-"+role] = 1

                    if str(p['stats']['item'+str(i)]) in mostlyUsedItems[role]:
                        participant["has-item-mostlyUsed-"+role] = 1

                    if str(p['stats']['item'+str(i)]) in underUsedItems[role]:
                        participant["has-item-underUsed-"+role] = 1
        
        
        #Summoner spells
        participant = {**participant, **spells}
        participant["spell-"+str(p["spell1Id"])] = 1
        participant["spell-"+str(p["spell2Id"])] = 1
        
        #Player stats
        participant = {**participant, **playerStats[str(participantId)]}
        
        participant["participantId"] = participantId
        
        participantList.append(participant)
        '''
        position = roleml_model.predict([participant])
        
        participantRoles[participantId] = position
        '''
    df = pd.DataFrame(participantList)
    df["role"] = roleml_model.predict(df.drop(["participantId"], axis=1))
    
    df = df.set_index(df["participantId"])
    
    participantRoles = df["role"].to_dict()
    
    return participantRoles