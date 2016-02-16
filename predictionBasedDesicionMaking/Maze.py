class Maze:
  START_STATE = "S"
  KEY_STATE = "K"
  GOAL_STATE = "G"
  CHOICE_STATE = "C"
  END_STATE = "E"
  

  def __init__(self):
    self.reset()
    self.AllStates = [self.START_STATE, self.END_STATE, self.KEY_STATE, self.GOAL_STATE, self.CHOICE_STATE]

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
    if state == self.START_STATE:
      return [self.CHOICE_STATE]
    elif state == self.KEY_STATE:
      return [self.CHOICE_STATE]
    elif state == self.GOAL_STATE:
      return [self.END_STATE]
    elif state == self.END_STATE:
      return []
    elif state == self.CHOICE_STATE:
      return [self.KEY_STATE, self.GOAL_STATE]
    else:
      raise ValueError("{} state is not recognized", state)
    
  def getRewardFor(self, state):
    if state == self.GOAL_STATE:
      return 1# if self.keyVisited else -1
    else:
       return 0
