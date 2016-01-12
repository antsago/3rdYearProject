from Maze import Maze
from HTMModel import HTMModel
from Agent import Agent
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
  

if __name__ == "__main__":
  for mazeLength in [1, 2, 13]:
    print "-- New maze run with lenght {} --".format(mazeLength)
    maze = Maze(mazeLength)
    htmModel = HTMModel(maze.AllStates)
    tdModel = QLearningModel(maze.AllStates)
    tdAgent = Agent(maze, tdModel)
    htmAgent = Agent(maze, htmModel)
    tdPerformance = tdAgent.run()
    print "tdPerfomance"
    print tdPerformance
    print ">>change agent"
    htmPerformance = htmAgent.run()
    print "htmPerformance"
    print htmPerformance
