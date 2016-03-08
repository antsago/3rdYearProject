import unittest
from src import ConfusionMatrix

class TestConfusionMatrix(unittest.TestCase):

  def test_whenInitializedCountIsZero(self):
    rewardClasses = [0,1]
    confusionMatrix = ConfusionMatrix(rewardClasses)
    for realReward in rewardClasses:
      for predictedReward in rewardClasses:
        self.assertEqual(0, confusionMatrix.confusionMatrix[realReward][predictedReward])

  def test_whenObservationIsAddedCountIncreasesByOne(self):
    rewardClasses = [0,1]
    confusionMatrix = ConfusionMatrix(rewardClasses)
    realReward = 0
    predictedReward = 0

    confusionMatrix.addObservation(realReward, predictedReward)
    
    self.assertEqual(1, confusionMatrix.confusionMatrix[realReward][predictedReward])

  def test_whenConfusionMatrixAreMergedCountsAreAdded(self):
    rewardClasses = [0,1]
    confusionMatrix1 = ConfusionMatrix(rewardClasses)
    confusionMatrix2 = ConfusionMatrix(rewardClasses)
    realReward = 0
    predictedReward = 0
    confusionMatrix2.addObservation(realReward, predictedReward)

    confusionMatrix1.merge(confusionMatrix2)

    self.assertEqual(1, confusionMatrix1.confusionMatrix[realReward][predictedReward])

  def test_whenAllPredictionsAreCorrectAccuracyIs100(self):
    rewardClasses = [0,1]
    confusionMatrix = ConfusionMatrix(rewardClasses)
    realReward = 0
    predictedReward = 0
    confusionMatrix.addObservation(realReward, predictedReward)
    
    self.assertEqual(100, confusionMatrix.accuracy())

  def test_whenNoPredictionIsCorrectAccuracyIs0(self):
    rewardClasses = [0,1]
    confusionMatrix = ConfusionMatrix(rewardClasses)
    realReward = 0
    predictedReward = 1
    confusionMatrix.addObservation(realReward, predictedReward)
    
    self.assertEqual(0, confusionMatrix.accuracy())

