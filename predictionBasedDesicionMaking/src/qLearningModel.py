from random import random, choice

class QLearningModel:
  INITIAL_VALUE = 1

  def __init__(self, listOfStates, learningStep = 0.1, discountingFactor = 0.9):
    self.valueTable = { state: self.INITIAL_VALUE for state in listOfStates}
    self.learningStep = learningStep
    self.discountingFactor = discountingFactor

  def problemFinished(self):
    pass

  def makeMove(self, currentState, currentStateReward, nextState):
    discountedValue = max(self.discountingFactor * self.valueTable[nextState], currentStateReward)
    valueError = discountedValue - self.valueTable[currentState]
    self.valueTable[currentState] += self.learningStep * valueError
    return int(self.valueTable[nextState])

  def predictRewards(self, currentState, currentStateReward, nextPossibleStates):
    return { state: self.valueTable[state] for state in nextPossibleStates }
  
