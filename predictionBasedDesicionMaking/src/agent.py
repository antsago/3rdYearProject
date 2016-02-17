from random import choice, random
from confusionMatrix import ConfusionMatrix

class Agent:

  def __init__(self, maze, model, epsilon = 0.3):
    self.model = model
    self.maze = maze
    self.epsilon = epsilon
    self.predictedReward = 0

  def solveMaze(self, noTimes):
    self.confusionMatrix = ConfusionMatrix(self.maze.POSSIBLE_REWARDS)

    for iteration in range(noTimes):
      self._solveMaze()

    return self.confusionMatrix

  def _solveMaze(self):
    self._moveUntilMazeIsSolved()
    self.model.problemFinished()
    self.maze.reset()
  
  def _moveUntilMazeIsSolved(self):
    mazeSolvedInStep = 0
    accumulatedReward = 0
    while self.maze.isNotFinished():
      accumulatedReward += self._makeMove()
      mazeSolvedInStep += 1
    return mazeSolvedInStep, accumulatedReward
 
  def _makeMove(self):
    nextPossibleStates = self.maze.getPossibleActions()
    currentStateReward = self.maze.getReward()
    self.confusionMatrix.addObservation(currentStateReward, self.predictedReward)

    nextState = self._epsilonGreedy(self.maze.currentState, currentStateReward, nextPossibleStates)
    self.predictedReward = self._moveTo(self.maze.currentState, currentStateReward, nextState) 
    return currentStateReward

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

