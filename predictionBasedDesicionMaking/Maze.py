class Maze:
  START_STATE = "S"
  KEY_STATE = "K"
  GOAL_STATE = "G"
  END_STATE = "E"
  

  def __init__(self, noStates):
    self.reset()
    self.SimpleStates = range(noStates)
    self.AllStates = self.SimpleStates + [self.START_STATE, self.END_STATE, self.KEY_STATE, self.GOAL_STATE]

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
      return self.SimpleStates + [self.KEY_STATE, self.GOAL_STATE]
    elif state == self.KEY_STATE:
      return self.SimpleStates
    elif state == self.GOAL_STATE:
      return [self.END_STATE]
    elif state == self.END_STATE:
      return []
    else:
      return self.SimpleStates[0:state] + self.SimpleStates[state+1:len(self.SimpleStates)] + [self.KEY_STATE, self.GOAL_STATE]
    
  def getRewardFor(self, state):
    if state == self.GOAL_STATE:
      return 1 if self.keyVisited else -1
    else:
       return 0
