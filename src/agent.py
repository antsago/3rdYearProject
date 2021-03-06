from random import choice, random, SystemRandom
from performanceRecord import PerformanceRecord

class Agent:

  def __init__(self, maze, model, epsilonPolicy):
    self.model = model
    self.maze = maze
    self.random = SystemRandom()
    self.epsilonPolicy = epsilonPolicy

  def solveMaze(self, noTimes):
    return {iteration: self._solveMaze(iteration) for iteration in range(1, noTimes + 1)}

  def _solveMaze(self,iteration):
    performance = self._moveUntilMazeIsSolved(iteration)
    self.model.problemFinished()
    self.maze.reset()

    return performance
  
  def _moveUntilMazeIsSolved(self, iteration):
    self.epsilon = self.epsilonPolicy(iteration) 
    performanceRecord = PerformanceRecord(self.maze.POSSIBLE_REWARDS)

    print "\n - Start new maze - "
    while self.maze.isNotFinished():
      currentStateReward, nextStatePredictedReward = self._makeMove()
      performanceRecord.recordMove(currentStateReward, nextStatePredictedReward)
      print "{}: Moved to {} with epsilon {}, reward {} and predictedReward {}".format(iteration, self.maze.currentState, self.epsilon, currentStateReward, nextStatePredictedReward)

    return performanceRecord
 
  def _makeMove(self):
    nextPossibleStates = self.maze.getPossibleActions()
    currentStateReward = self.maze.getReward()
    nextState = self._epsilonGreedy(self.maze.currentState, currentStateReward, nextPossibleStates)

    predictedReward = self._moveTo(self.maze.currentState, currentStateReward, nextState) 
    return currentStateReward, predictedReward

  def _epsilonGreedy(self, currentState, currentStateReward, nextPossibleStates):
    if self.random.random() > self.epsilon:
      predictedRewards = self.model.predictRewards(currentState, currentStateReward, nextPossibleStates)
      bestReward = max(predictedRewards.values())
      return self.random.choice([state for state in predictedRewards.keys() if predictedRewards[state] == bestReward])
    else:
      return self.random.choice(nextPossibleStates)

  def _moveTo(self, currentState, currentStateReward, nextState):
    self.maze.moveTo(nextState)
    return self.model.makeMove(currentState, currentStateReward, nextState)

