from Maze import Maze
from HTMModel import HTMModel
from Agent import Agent

class QLearningModel:
  INITIAL_VALUE = 1

  def __init__(self, listOfStates, learningStep = 0.1, discountingFactor = 0.9):
    self.valueTable = { state: self.INITIAL_VALUE for state in listOfStates}
    self.learningStep = learningStep
    self.discountingFactor = discountingFactor

  def problemFinished(self):
    pass

  def makeMove(self, currentState, currentStateReward, nextState):
    discountedValue = self.discountingFactor * self.valueTable[nextState] 
    valueError = discountedValue - self.valueTable[currentState]
    self.valueTable[currentState] += self.learningStep * valueError

  def predictRewards(self, currentState, currentStateReward, nextPossibleStates):
    return { state: self.valueTable[state] for state in nextPossibleStates }
  

if __name__ == "__main__":
  maze = Maze()
  htmModel = HTMModel(maze.STATES)
  tdModel = QLearningModel(maze.STATES)
  tdAgent = Agent(maze, tdModel)
  htmAgent = Agent(maze, htmModel)
  tdPerformance = tdAgent.run()
  print ">>Change agent"
  htmPerformance = htmAgent.run()
  print tdPerformance
  print htmPerformance
