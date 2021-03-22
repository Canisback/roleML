# Role ML

[![PyPi](https://img.shields.io/pypi/v/roleml)](https://pypi.org/project/roleml/)
[![Build Status](https://travis-ci.com/Canisback/roleml.svg?branch=master)](https://travis-ci.com/Canisback/roleml)
[![codecov](https://codecov.io/gh/Canisback/roleml/branch/master/graph/badge.svg)](https://codecov.io/gh/Canisback/roleml)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/github/Canisback/roleML.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Canisback/roleML/context:python)
[![Downloads](https://pepy.tech/badge/roleml)](https://pepy.tech/project/roleml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

***

## League of Legends Role Classifier

This project aims to provide to Riot Games API users, especially those using match data, a better classifier for role. It is known that the internal role classifier give a lot of misclassifications, making the whole thing not enough reliable for any production application.

Based on that observation, we used machine learning to create a classifier closer to what user would expect as roles, and with an improved accuracy. In order to get solid bases and verify the ability of our classifier, we build a set of manually labeled roles as a verification set. From this verification set, the Riot Games classifier gives a 12.5% error rate and our classifier downed this error rate to less than 0.1%, on really edge cases.

For more details about the development of the classifier, check https://github.com/Canisback/roleML/blob/master/exploration/Role%20ML.ipynb

To get the verification set raw data, get it here : https://github.com/Canisback/roleML/blob/master/data/verification_results.csv (column name is participantId) (all games are from EUW server).

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
import roleml
roleml.predict(match, timeline)
```
Output : 
```
{
 1: 'mid',
 2: 'bot',
 3: 'supp',
 4: 'top',
 5: 'jungle',
 6: 'top',
 7: 'jungle',
 8: 'bot',
 9: 'supp',
 10: 'mid'
}
```

The output is a dictionary linking participantId to their role.

The match needs to be at least 12 minutes long, an exception will be raised else.

### Options

Add the predicted role to the participant and fix the timeline data : 
```
fixed_match, fixed_timeline = 
	roleml.fix_game(game, timeline)
```

You can turn off the timeline fix : 
```
fixed_match, fixed_timeline = 
	roleml.fix_game(game, timeline, False)
```



You can also change the role format output : 
```
roleml.change_role_formatting("full")
```
 * clean (default)
```
{
 1: 'mid',
 2: 'bot',
 3: 'supp',
 4: 'top',
 5: 'jungle',
 6: 'top',
 7: 'jungle',
 8: 'bot',
 9: 'supp',
 10: 'mid'
}
```
 * full
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
 * rgapi
```
{
 1: {"lane":"MIDDLE","role":"SOLO"},
 2: {"lane":"BOTTOM","role":"DUO_CARRY"},
 3: {"lane":"BOTTOM","role":"DUO_SUPPORT"},
 4: {"lane":"TOP","role":"SOLO"},
 5: {"lane":"JUNGLE","role":"NONE"},
 6: {"lane":"TOP","role":"SOLO"},
 7: {"lane":"JUNGLE","role":"NONE"},
 8: {"lane":"BOTTOM","role":"DUO_CARRY"},
 9: {"lane":"BOTTOM","role":"DUO_SUPPORT"},
 10: {"lane":"MIDDLE","role":"SOLO"}
}
```

#### Cassiopeia support

RoleML partially supports Cassiopeia Match data structure. The predict function has a cassiopeia_dicts flag to be used with the Cassiopeia match .to_dict() function : 

```
roleml.predict(match.to_dict(), match.timeline.to_dict(), True)
```

A special function allows to add the predicited role in Participants object from Cassiopeia matches : 

```
roleml.add_cass_predicted_roles(match)
```


Working example : 

```
import roleml
import cassiopeia as cass

cass.set_riot_api_key("RGAPI-")
cass.set_default_region("EUW")

summoner = cass.get_summoner(name="Canisback")
match = cass.MatchHistory(summoner=summoner, queues={cass.Queue.blind_fives})[0].load()
match.timeline.load()

roleml.add_cass_predicted_roles(match)
for p in match.participants:
    print(p.predicted_role)
```

Output : 

```
bot
jungle
mid
top
supp
bot
mid
supp
jungle
top
```
