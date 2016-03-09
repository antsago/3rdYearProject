import unittest
from src import PerformanceResult
from src import PerformanceRecord

class TestPerformanceResult(unittest.TestCase):

  def test_whenIterationIsNewUserRecordConfusionMatrix(self):
    possibleRewards = [0,1]
    performanceRecord = PerformanceRecord(possibleRewards)
    performanceRecord.recordMove(1, 2)
    
    performanceResult = PerformanceResult()
    iteration = 1
    performanceResult.addRecord(iteration, performanceRecord)

    self.assertEqual(performanceRecord.confusionMatrix, performanceResult.results[iteration]["ConfusionMatrix"])

  def test_whenIterationExistsMergeConfusionMatrices(self):
    possibleRewards = [0,1]
    performanceRecord1 = PerformanceRecord(possibleRewards)
    performanceRecord1.recordMove(0, 0)
    performanceRecord2 = PerformanceRecord(possibleRewards)
    performanceRecord2.recordMove(1, 1)
    
    iteration = 1
    performanceResult = PerformanceResult()
    performanceResult.addRecord(iteration, performanceRecord1)
    performanceResult.addRecord(iteration, performanceRecord2)
    
    self.assertEqual(1, performanceResult.results[iteration]["ConfusionMatrix"].confusionMatrix[1][0])
    self.assertEqual(1, performanceResult.results[iteration]["ConfusionMatrix"].confusionMatrix[0][0])

  def test_whenRecordIsAddedAccumulatedRewardIsAppended(self):
    possibleRewards = [0,2,1]
    performanceRecord1 = PerformanceRecord(possibleRewards)
    performanceRecord1.recordMove(1, 1)
    performanceRecord2 = PerformanceRecord(possibleRewards)
    performanceRecord2.recordMove(2, 1)
    
    iteration = 1
    performanceResult = PerformanceResult()
    performanceResult.addRecord(iteration, performanceRecord1)
    performanceResult.addRecord(iteration, performanceRecord2)
    
    self.assertEqual(1, performanceResult.results[iteration]["AccumulatedReward"][0])
    self.assertEqual(2, performanceResult.results[iteration]["AccumulatedReward"][1])

  def test_whenRecordIsAddedVisitedStatesIsAppended(self):
    possibleRewards = [0,2,1]
    performanceRecord1 = PerformanceRecord(possibleRewards)
    performanceRecord1.recordMove(1, 1)
    performanceRecord2 = PerformanceRecord(possibleRewards)
    performanceRecord2.recordMove(2, 1)
    performanceRecord2.recordMove(2, 1)
    
    iteration = 1
    performanceResult = PerformanceResult()
    performanceResult.addRecord(iteration, performanceRecord1)
    performanceResult.addRecord(iteration, performanceRecord2)
    
    self.assertEqual(0, performanceResult.results[iteration]["NoVisitedStates"][0])
    self.assertEqual(1, performanceResult.results[iteration]["NoVisitedStates"][1])

