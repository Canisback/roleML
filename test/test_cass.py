try:
    import roleml
    import json
    import os

    from cassiopeia.dto.match import MatchDto, TimelineDto
    from cassiopeia.core.match import MatchData, Match, TimelineData, Timeline
    from cassiopeia.transformers.match import MatchTransformer

    def create_Cass_match(data):
        match_transformer = MatchTransformer()

        match_dto = MatchDto(data)
        match_data = match_transformer.transform(MatchData, match_dto)

        timeline_dto = TimelineDto(data["timeline"])
        timeline_data = match_transformer.transform(TimelineData, timeline_dto)

        match = Match.from_data(match_data)
        timeline = Timeline.from_data(timeline_data)
        match._timeline = timeline

        return match

    def test_predict_1():
        with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
            data = json.load(f)

        roles = {
            1: 'supp',
            2: 'jungle',
            3: 'top',
            4: 'bot',
            5: 'mid',
            6: 'top',
            7: 'bot',
            8: 'supp',
            9: 'jungle',
            10: 'mid'
        }

        match = create_Cass_match(data)

        assert roles == roleml.predict(match.to_dict(), match.timeline.to_dict(), True)


    def test_predict_2():
        with open(os.path.dirname(__file__) + "/data/EUW-3692606327.json", "r") as f:
            data = json.load(f)

        roles = {
            1: 'supp',
            2: 'top',
            3: 'mid',
            4: 'jungle',
            5: 'bot',
            6: 'top',
            7: 'supp',
            8: 'mid',
            9: 'jungle',
            10: 'bot'
        }

        match = create_Cass_match(data)

        assert roles == roleml.predict(match.to_dict(), match.timeline.to_dict(), True)

    def test_predict_match_too_short():
        with open(os.path.dirname(__file__) + "/data/EUW-4236896092.json", "r") as f:
            data = json.load(f)

        match = create_Cass_match(data)

        try:
            roleml.predict(match.to_dict(), match.timeline.to_dict(), True)
            assert False
        except:
            assert True



    def test_add_cass_predicited_roles():

        with open(os.path.dirname(__file__) + "/data/NA-3023745286.json", "r") as f:
            data = json.load(f)

        roles = {
            1: 'supp',
            2: 'jungle',
            3: 'top',
            4: 'bot',
            5: 'mid',
            6: 'top',
            7: 'bot',
            8: 'supp',
            9: 'jungle',
            10: 'mid'
        }

        match = create_Cass_match(data)

        roleml.add_cass_predicited_roles(match)

        for p in match.participants:
            assert p.predicted_role == roles[p.id]
except:
    import warnings
    warnings.warn("Cassiopeia support is not tested because of pytest/travis")