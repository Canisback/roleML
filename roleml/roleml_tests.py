import unittest
from sklearn.externals import joblib
from roleml import roleml


class TestRoleML(unittest.TestCase):
    # This is a list of 50 tuples containing responses from match-v4.
    # Position 0 is the game, position 1 is its timeline, position 2 is the result
    games_timelines_results = joblib.load('games_timelines_results.pkl.z')

    def test_predict(self):
        for game, timeline, result in self.games_timelines_results:
            self.assertDictEqual(roleml.predict(game, timeline), result)

    def test_fix_game_and_timeline(self):
        # Doing an existence test to test that the new values are properly here
        for game, timeline, result in self.games_timelines_results:
            game_fixed, timeline_fixed = roleml.fix_and_augment_game_and_timeline(game, timeline)

            for participant in game_fixed['participants']:
                self.assertIsNotNone(participant['role'])

            for frame in timeline_fixed['frames']:
                for participantFrame in frame['participantFrames'].values():
                    self.assertIsNotNone(participantFrame['totalGoldDiff'])
                    self.assertIsNotNone(participantFrame['xpDiff'])
                    self.assertIsNotNone(participantFrame['minionsKilledDiff'])
                    self.assertIsNotNone(participantFrame['totalGoldDiff'])


if __name__ == '__main__':
    unittest.main()

