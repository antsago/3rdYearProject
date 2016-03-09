from maze import Maze

class FirstOrderImmediateProblem(Maze):
  POSSIBLE_REWARDS = [0,1]
  CHOICE_STATE = "C"

  def __init__(self):
    Maze.__init__(self)
    self.AllStates = [self.START_STATE, self.END_STATE, self.KEY_STATE, self.GOAL_STATE, self.CHOICE_STATE]
  
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
      return 1
    else:
       return 0
