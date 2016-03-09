from confusionMatrix import ConfusionMatrix

class PerformanceRecord:
  
  def __init__(self, possibleRewards):
    self.confusionMatrix = ConfusionMatrix(possibleRewards)
    self.accumulatedReward = 0
    self.noVisitedStates = -1 # to exclude start and end
    self.predictedReward = 0

  def recordMove(self, currentStateReward, nextStatePredictedReward):
    self.noVisitedStates += 1
    self.accumulatedReward += currentStateReward
    self.confusionMatrix.addObservation(currentStateReward, self.predictedReward)
    self.predictedReward = nextStatePredictedReward
