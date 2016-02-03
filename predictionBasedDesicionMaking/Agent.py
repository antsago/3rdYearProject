from random import choice

class Agent:

  def __init__(self, maze, model, trainingIterations, testingIterations):
    self.model = model
    self.maze = maze
    self.trainingIterations = trainingIterations
    self.testingIterations = testingIterations

  def run(self):  
    trainPerformance = self.trainModel(self.trainingIterations)
    testPerformance = self.testModel(self.testingIterations)
    return trainPerformance, testPerformance
  
  def trainModel(self, trainIterations):
    self.model.setTrainPolicy()
    return self.iterateMaze(trainIterations)
  
  def testModel(self, testIterations):
    self.model.setTestPolicy()
    return self.iterateMaze(testIterations)
  
  def iterateMaze(self, noIterations):
    performanceHistory = []
    for iteration in range(noIterations):
      iterationPerformance = self.solveMaze()
      self.model.problemFinished()
      self.maze.reset()
      performanceHistory.append([iteration, iterationPerformance])
    return performanceHistory
  
  def solveMaze(self):
    mazeSolvedInStep = 0
    accumulatedReward = 0
    while self.maze.isNotFinished():
      accumulatedReward += self._performMazeIteration()
      mazeSolvedInStep += 1
    return mazeSolvedInStep, accumulatedReward
 
  def _performMazeIteration(self):
      nextPossibleStates = self.maze.getPossibleActions()
      currentStateReward = self.maze.getReward()
      nextState = self.model.policy(self.maze.currentState, currentStateReward, nextPossibleStates)
      print "Move from {} to {} with reward {} and possible states {}".format(self.maze.currentState, nextState, currentStateReward, nextPossibleStates)
      self.moveTo(self.maze.currentState, currentStateReward, nextState) 
      return currentStateReward

  def moveTo(self, currentState, currentStateReward, nextState):
    self.maze.moveTo(nextState)
    self.model.makeMove(currentState, currentStateReward, nextState)

