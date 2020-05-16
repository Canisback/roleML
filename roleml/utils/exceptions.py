class MatchTooShort(Exception):
    def __init__(self):
        Exception.__init__(self,"Match too short, needs at least 720 seconds")
        
class IncorrectMap(Exception):
    def __init__(self):
        Exception.__init__(self, "Map does not match, needs Summoner's Rift")

class WrongLabel(Exception):
    def __init__(self):
        Exception.__init__(self, 'Label needs to be "clean", "rgapi" or "full"')