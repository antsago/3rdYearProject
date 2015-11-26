from random import choice

class Agent:
  DEFAULT_TRAINING_ITERATIONS = 500
  DEFAULT_TEST_ITERATIONS = 500

  def __init__(self, maze, model):
    self.model = model
    self.maze = maze

  def run(self):  
    self.trainModel(2)
    print "### End training, start testing ###"
    self.testModel(2)
  
  def trainModel(self, trainIterations):
    self.iterateMaze(self.randomPolicy, trainIterations)
  
  def testModel(self, testIterations):
    self.iterateMaze(self.bestNextStatePolicy, testIterations)
  
  def iterateMaze(self, policy, noIterations):
    for iteration in range(noIterations):
      self.solveMaze(policy, iteration)
      self.model.problemFinished()
      self.maze.reset()
  
  def solveMaze(self, policy, iteration):
    while self.maze.isNotFinished():
      nextPossibleStates = self.maze.getPossibleActions()
      currentStateReward = self.maze.getReward()
      nextState = policy(self.maze.currentState, currentStateReward, nextPossibleStates)
      self.moveTo(self.maze.currentState, currentStateReward, nextState)
      print "At iteration {} took move to state {}".format(iteration, nextState)

  def moveTo(self, currentState, currentStateReward, nextState):
    self.maze.moveTo(nextState)
    self.model.makeMove(currentState, currentStateReward, nextState)

  def bestNextStatePolicy(self, currentState, currentStateReward, nextPossibleStates):
    predictedRewards = self.model.predictRewards(currentState, currentStateReward, nextPossibleStates)
    bestReward = max(predictedRewards.values())
    return choice([state for state in predictedRewards.keys() if predictedRewards[state] == bestReward])
  
  def randomPolicy(self, currentState, currentStateReward, nextPossibleStates):
    return choice(nextPossibleStates)

