class Maze:
  START_STATE = "S"
  GOAL_STATE = "G"
  KEY_STATE = "K"
  END_STATE = "E"
  
  STATES = [START_STATE, GOAL_STATE, KEY_STATE, END_STATE, "C"]

  POSSIBLE_ACTIONS_FROM = \
  {
    "S": ["C"],
    "C": ["K", "G"],
    "K": ["C"],
    "G": ["E"],
  }
            
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
  
  def getPossibleActionsFrom(self, state):
    return self.POSSIBLE_ACTIONS_FROM[state]
    
  def getRewardFor(self, state):
    if state == self.GOAL_STATE:
      return 1 if self.keyVisited else -1
    else:
       return 0
