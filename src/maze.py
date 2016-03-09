class Maze:
  START_STATE = "S"
  KEY_STATE = "K"
  GOAL_STATE = "G"
  END_STATE = "E"
  
  def __init__(self):
    self.reset()

  def isNotFinished(self):
    return self.currentState != self.END_STATE

  def getPossibleActions(self):
    return self.getPossibleActionsFrom(self.currentState)

  def getReward(self):
    return self.getRewardFor(self.currentState)

  def moveTo(self, nextState):
    if self._moveIsNotValid(nextState):
      raise ValueError("{} is not a valid move from {}", nextState, self.currentState)
    self.currentState = nextState
    if self.currentState == self.KEY_STATE:
      self.keyVisited = True

  def reset(self):
    self.currentState = self.START_STATE
    self.keyVisited = False

  def _moveIsNotValid(self, nextState):
    return nextState not in self.getPossibleActions()
