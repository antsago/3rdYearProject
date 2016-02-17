from json import JSONEncoder


class ConfusionMatrix(JSONEncoder):

  def __init__(self, rewardClasses):
    #outer loop, real/true reward, inner is predicted reward
    self.confusionMatrix = {realReward: {predictedReward: 0 for predictedReward in rewardClasses}
                                     for realReward in rewardClasses}
    self.rewardClasses = rewardClasses

  def addObservation(self, real, predicted):
    self.confusionMatrix[real][predicted] += 1
  
  def merge(self, other):
    if other.rewardClasses != self.rewardClasses:
      raise ValueError("Merged confusion matrix has {} as classes instead of {}",
		 other.rewardClasses, self.rewardClasses)
    for real in self.rewardClasses:
      for predicted in self.rewardClasses:
        self.confusionMatrix[real][predicted] += other.confusionMatrix[real][predicted]

  def accuracy(self):
    predictedPopulation = sum([self.confusionMatrix[rewClass][rewClass] 
                               for rewClass in self.rewardClasses])
    totalPopulation = sum([sum([self.confusionMatrix[real][predicted]
                               for predicted in self.rewardClasses]) for real in self.rewardClasses])
    return 100 * predictedPopulation / totalPopulation if totalPopulation > 0 else 0

  def recall(self, askedClass):
    classPopulation = sum([self.confusionMatrix[askedClass][predicted]
			 for predicted in self.rewardClasses])
    return 100 * self.confusionMatrix[askedClass][askedClass] / classPopulation if classPopulation > 0 else 0 

  def precision(self, askedClass):
    noPredictions = sum([self.confusionMatrix[real][askedClass] for real in self.rewardClasses])
    return 100 * self.confusionMatrix[askedClass][askedClass] / noPredictions if noPredictions > 0 else 0 

  def toJSON(self):
    return {"ConfusionMatrix": self.confusionMatrix,
            "RewardClasses": self.rewardClasses,
            "Accuracy": self.accuracy(),
            "Precision": {rewardClass: self.precision(rewardClass) for rewardClass in self.rewardClasses},
            "Recall": {rewardClass: self.recall(rewardClass) for rewardClass in self.rewardClasses},
            }
