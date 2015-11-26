from random import choice

class Agent:
  DEFAULT_TRAINING_ITERATIONS = 500
  DEFAULT_TEST_ITERATIONS = 500

  def __init__(self, maze, model):
    self.model = model
    self.maze = maze

  def run(self):  
    trainPerformance = self.trainModel(self.DEFAULT_TRAINING_ITERATIONS)
    testPerformance = self.testModel(self.DEFAULT_TEST_ITERATIONS)
    return trainPerformance, testPerformance
  
  def trainModel(self, trainIterations):
    return self.iterateMaze(self.randomPolicy, trainIterations)
  
  def testModel(self, testIterations):
    return self.iterateMaze(self.bestNextStatePolicy, testIterations)
  
  def iterateMaze(self, policy, noIterations):
    performanceHistory = []
    for iteration in range(noIterations):
      iterationPerformance = self.solveMaze(policy)
      self.model.problemFinished()
      self.maze.reset()
      performanceHistory.append([iteration, iterationPerformance])
    return performanceHistory
  
  def solveMaze(self, policy):
    mazeSolvedInStep = 0
    while self.maze.isNotFinished():
      self._performMazeIteration(policy)
      mazeSolvedInStep += 1
    return mazeSolvedInStep
 
  def _performMazeIteration(self, policy):
      nextPossibleStates = self.maze.getPossibleActions()
      currentStateReward = self.maze.getReward()
      nextState = policy(self.maze.currentState, currentStateReward, nextPossibleStates)
      self.moveTo(self.maze.currentState, currentStateReward, nextState) 

  def moveTo(self, currentState, currentStateReward, nextState):
    self.maze.moveTo(nextState)
    self.model.makeMove(currentState, currentStateReward, nextState)

  def bestNextStatePolicy(self, currentState, currentStateReward, nextPossibleStates):
    predictedRewards = self.model.predictRewards(currentState, currentStateReward, nextPossibleStates)
    bestReward = max(predictedRewards.values())
    return choice([state for state in predictedRewards.keys() if predictedRewards[state] == bestReward])
  
  def randomPolicy(self, currentState, currentStateReward, nextPossibleStates):
    return choice(nextPossibleStates)

