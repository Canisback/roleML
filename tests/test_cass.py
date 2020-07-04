skip_cass = False

try:
    import cassiopeia
    from cassiopeia.core.match import MatchData, Match, TimelineData, Timeline
    from cassiopeia.dto.match import MatchDto, TimelineDto
    from cassiopeia.transformers.match import MatchTransformer
except ModuleNotFoundError:
    import warnings

    warnings.warn("Cassiopeia support was not tested because of pytest/travis")
    # TODO Quit
    # assert False
    skip_cass = True


import pytest
import roleml


def create_cass_match(data):
    match_transformer = MatchTransformer()

    match_dto = MatchDto(data)
    match_data = match_transformer.transform(MatchData, match_dto)

    timeline_dto = TimelineDto(data["timeline"])
    timeline_data = match_transformer.transform(TimelineData, timeline_dto)

    match = Match.from_data(match_data)
    timeline = Timeline.from_data(timeline_data)
    match._timeline = timeline

    return match

@pytest.mark.skipif(skip_cass, reason="Travis")
def test_predict_1(clean_game_na):
    match = create_cass_match(clean_game_na["game"])
    assert clean_game_na["expected_roles"] == roleml.predict(match.to_dict(), match.timeline.to_dict(), True)


@pytest.mark.skipif(skip_cass, reason="Travis")
def test_predict_2(clean_game_euw):
    match = create_cass_match(clean_game_euw["game"])

    assert clean_game_euw["expected_roles"] == roleml.predict(match.to_dict(), match.timeline.to_dict(), True)


@pytest.mark.skipif(skip_cass, reason="Travis")
def test_predict_match_too_short(short_game):
    match = create_cass_match(short_game["game"])

    with pytest.raises(roleml.exceptions.MatchTooShort):
        roleml.predict(match.to_dict(), match.timeline.to_dict(), True)


@pytest.mark.skipif(skip_cass, reason="Travis")
def test_add_cass_predicted_roles(clean_game_na):
    match = create_cass_match(clean_game_na["game"])

    roleml.add_cass_predicted_roles(match)

    for p in match.participants:
        assert p.predicted_role == clean_game_na["expected_roles"][p.id]
