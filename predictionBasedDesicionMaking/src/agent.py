from random import choice, random
from performanceRecord import PerformanceRecord

class Agent:

  def __init__(self, maze, model, epsilon = 0.3):
    self.model = model
    self.maze = maze
    self.epsilon = epsilon

  def solveMaze(self, noTimes):
    return {iteration: self._solveMaze() for iteration in range(noTimes)}

  def _solveMaze(self):
    performance = self._moveUntilMazeIsSolved()
    self.model.problemFinished()
    self.maze.reset()

    return performance
  
  def _moveUntilMazeIsSolved(self):
    performanceRecord = PerformanceRecord(self.maze.POSSIBLE_REWARDS)

    while self.maze.isNotFinished():
      currentStateReward, nextStatePredictedReward = self._makeMove()
      performanceRecord.recordMove(currentStateReward, nextStatePredictedReward)

    return performanceRecord
 
  def _makeMove(self):
    nextPossibleStates = self.maze.getPossibleActions()
    currentStateReward = self.maze.getReward()
    nextState = self._epsilonGreedy(self.maze.currentState, currentStateReward, nextPossibleStates)

    predictedReward = self._moveTo(self.maze.currentState, currentStateReward, nextState) 
    return currentStateReward, predictedReward

  def _epsilonGreedy(self, currentState, currentStateReward, nextPossibleStates):
    if random <= self.epsilon:
      predictedRewards = self.model.predictRewards(currentState, currentStateReward, nextPossibleStates)
      bestReward = max(predictedRewards.values())
      return choice([state for state in predictedRewards.keys() if predictedRewards[state] == bestReward])
    else:
      return choice(nextPossibleStates)

  def _moveTo(self, currentState, currentStateReward, nextState):
    self.maze.moveTo(nextState)
    return self.model.makeMove(currentState, currentStateReward, nextState)

