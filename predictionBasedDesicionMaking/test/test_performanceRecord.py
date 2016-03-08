import unittest
from src import PerformanceRecord

class TestPerformanceRecord(unittest.TestCase):

  def test_whenInitializedRecordsAreZero(self):
    possibleRewards = [0,1]
    performanceRecord = PerformanceRecord(possibleRewards)

    self.assertEqual(0, performanceRecord.accumulatedReward)
    self.assertEqual(-1, performanceRecord.noVisitedStates)
    self.assertEqual(0, performanceRecord.predictedReward)

  def test_whenMoveRecordedNoVisitedStatesIncreases(self):
    possibleRewards = [0,1]
    performanceRecord = PerformanceRecord(possibleRewards)
    currentReward = 1
    nextStatePredictedReward = 2
    performanceRecord.recordMove(currentReward, nextStatePredictedReward)
    
    self.assertEqual(0, performanceRecord.noVisitedStates)

  def test_whenMoveRecordedCurrentRewardIsAddedToAccumulatedReward(self):
    possibleRewards = [0,1]
    performanceRecord = PerformanceRecord(possibleRewards)
    currentReward = 1
    nextStatePredictedReward = 2
    performanceRecord.recordMove(currentReward, nextStatePredictedReward)
    
    self.assertEqual(1, performanceRecord.accumulatedReward)

  def test_whenMoveRecordedPredictedRewardIsRemmembered(self):
    possibleRewards = [0,1]
    performanceRecord = PerformanceRecord(possibleRewards)
    currentReward = 1
    nextStatePredictedReward = 2
    performanceRecord.recordMove(currentReward, nextStatePredictedReward)
    
    self.assertEqual(nextStatePredictedReward, performanceRecord.predictedReward)
