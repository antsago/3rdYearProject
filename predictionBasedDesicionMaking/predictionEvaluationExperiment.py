from src import SecondOrderImmediateProblem, FirstOrderImmediateProblem, HTMModel, Agent, QLearningModel, PerformanceResult
import json

def main():
  noTrials = 1000
  noIterations = 300
  
  performance = PerformanceResult()
  for trial in range(noTrials):
    maze = FirstOrderImmediateProblem()
    model = QLearningModel(maze.AllStates) #HTMModel(maze.AllStates)
    agent = Agent(maze, model, degradeEpsilon = False, initialEpsilon = 0)
    iterationPerformance = agent.solveMaze(noIterations)
    performance.addTrialRecords(iterationPerformance)
  
  with open("firsImPredResults.json", "w") as resultsFile:
    resultsFile.write(json.dumps(performance.toJSON()))

if __name__ == "__main__":
  main()
