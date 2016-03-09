import unittest
from src import QLearningModel

class TestQLearningModel(unittest.TestCase):

  def test_predictRewardsReturnsTableValue(self):
    qModel = QLearningModel(["A"])
    stateValue = 2
    qModel.valueTable["A"] = stateValue

    predictedRewards = qModel.predictRewards(None,None,["A"])
    self.assertEqual(stateValue, predictedRewards["A"])

  def test_whenRewardIsEqualToTableValueValueDoNotChange(self):
    qModel = QLearningModel(["A", "B"])
    stateValue = 2
    qModel.valueTable["A"] = stateValue

    qModel.makeMove("A", stateValue, "B")
    self.assertEqual(stateValue, qModel.valueTable["A"])

  def test_whenRewardIsLessThanValueValueIsDiscounted(self):
    qModel = QLearningModel(["A", "B"])
    stateValue = 1
    qModel.valueTable["A"] = stateValue

    qModel.makeMove("A", stateValue - 1, "B")
    self.assertTrue(stateValue > qModel.valueTable["A"])

