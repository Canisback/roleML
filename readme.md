# Role ML


This project aims to provide to Riot Games API users, especially those using match data, a better classifier for role. It is known that the internal role classifier give a lot of misclassifications, making the whole thing not enough reliable for any production application.

Based on that observation, we used machine learning to create a classifier closer to what user would expect as roles, and with an improved accuracy. In order to get solid bases and verify the ability of our classifier, we build a set of manually labeled roles as a verification set. From this verification set, the Riot Games classifier gives a 12.5% error rate and our classifier downed this error rate to less than 0.1%, on really edge cases.

For more details about the development of the classifier, check https://github.com/Canisback/roleML/blob/master/Role%20ML.ipynb

To get the verification set raw data, get it here : https://github.com/Canisback/roleML/blob/master/verification_set.csv (column name is participantId) (all games are from EUW server).

This classifier only works for normal and ranked games on Summoner's Rift.

Note that the range of possible role as been reduced to the 5 most used roles : MIDDLE_SOLO, TOP_SOLO, JUNGLE_NONE, BOTTOM_DUO_CARRY, BOTTOM_DUO_SUPPORT.

***
## How to use it

The classifier is available as a python module.
```
pip install roleml
```

As the classifier relies on a set of carefully picked features from the match data, you will need to give it raw data from the API : 
 * Match  : https://developer.riotgames.com/api-methods/#match-v4/GET_getMatch
 * Timeline : https://developer.riotgames.com/api-methods/#match-v4/GET_getMatchTimeline

```
from roleml import roleml
roleml.predict(match, timeline)
```
Output : 
```
{
 1: 'MIDDLE_SOLO',
 2: 'BOTTOM_DUO_CARRY',
 3: 'BOTTOM_DUO_SUPPORT',
 4: 'TOP_SOLO',
 5: 'JUNGLE_NONE',
 6: 'TOP_SOLO',
 7: 'JUNGLE_NONE',
 8: 'BOTTOM_DUO_CARRY',
 9: 'BOTTOM_DUO_SUPPORT',
 10: 'MIDDLE_SOLO'
}
```

The output is a dictionary linking participantId to their role.

The match needs to be at least 12 minutes long, an exception will be raised else.

### Options

Fix match data according to the new participant roles : 
```
fixed_match, fixed_timeline = 
	roleml.fix_and_augment_game_and_timeline(game, timeline)
```
Add role to participant and goldDiffPerMinDeltas to participant timeline : 
```
fixed_and_augmented_match, fixed_timeline = 
	roleml.fix_and_augment_game_and_timeline(game, timeline, True)
```
Add diffs to each participant frame in timeline : 
```
fixed_match, fixed_and_augmented_timeline = 
	roleml.fix_and_augment_game_and_timeline(game, timeline, False, True)
```
Fix and augment both : 
```
fixed_and_augmented_match, fixed_and_augmented_timeline = 
	roleml.fix_and_augment_game_and_timeline(game, timeline, True, True)
```