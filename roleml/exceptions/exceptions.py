class MatchTooShort(Exception):
    def __init__(self):
        Exception.__init__(self, "This package only works with games over 15 minutes.")


class IncorrectMap(Exception):
    def __init__(self):
        Exception.__init__(self, "This package only handles Summoner’s Rift games.")


class WrongLabel(Exception):
    def __init__(self):
        Exception.__init__(self, 'Label needs to be in ["clean", "rgapi", "full", "LolGame"]')


class NoOpponentFoundException(Exception):
    pass
