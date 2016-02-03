from random import random, choice

class QLearningModel:
  INITIAL_VALUE = 1

  def __init__(self, listOfStates, learningStep = 0.1, discountingFactor = 0.9, epsilon = 0.3):
    self.valueTable = { state: self.INITIAL_VALUE for state in listOfStates}
    self.learningStep = learningStep
    self.discountingFactor = discountingFactor
    self.epsilon = epsilon
    self.policy = self.epsilonGreedyPolicy

  def setTrainPolicy(self):
    pass
  
  def setTestPolicy(self):
    pass

  def epsilonGreedyPolicy(self, currentState, currentStateReward, nextPossibleStates):
    if random <= self.epsilon:
      predictedRewards = self.predictRewards(currentState, currentStateReward, nextPossibleStates)
      bestReward = max(predictedRewards.values())
      return choice([state for state in predictedRewards.keys() if predictedRewards[state] == bestReward])
    else:
      return choice(nextPossibleStates)

  def problemFinished(self):
    pass

  def makeMove(self, currentState, currentStateReward, nextState):
    discountedValue = self.discountingFactor * self.valueTable[nextState] 
    valueError = discountedValue - self.valueTable[currentState]
    self.valueTable[currentState] += self.learningStep * valueError

  def predictRewards(self, currentState, currentStateReward, nextPossibleStates):
    return { state: self.valueTable[state] for state in nextPossibleStates }
  
