from src import FirstOrderProblem, HTMModel


def main():
  problem = FirstOrderProblem()
  htm = HTMModel(problem.AllStates)
  
  confusionMatrix = ConfusionMatrix()

def solveMaze()
  def _makeMove(self):
    nextPossibleStates = maze.getPossibleActions()
    currentStateReward = maze.getReward()
    confusionMatrix.addObservation(currentStateReward, predictedReward)
    nextState = choice(nextPossibleStates)
    predictedReward = self._moveTo(self.maze.currentState, currentStateReward, nextState) 
    
    return currentStateReward
 next  

  def _moveTo(self, currentState, currentStateReward, nextState):
    self.maze.moveTo(nextState)
    self.model.makeMove(currentState, currentStateReward, nextState)
  

if __name__ == "__main__":
  main()
