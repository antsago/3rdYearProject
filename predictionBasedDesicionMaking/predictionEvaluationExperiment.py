from src import SecondOrderImmediateProblem, FirstOrderImmediateProblem, HTMModel, Agent, QLearningModel, PerformanceResult, MultiStepProblem
import json

def main():
  noTrials = 1500
  noIterations = 50
  
  performance = PerformanceResult()
  for trial in range(noTrials):
    maze = MultiStepProblem()#FirstOrderImmediateProblem()
    model = HTMModel(maze.AllStates)
    agent = Agent(maze, model, degradeEpsilon = False, initialEpsilon = 1)
    iterationPerformance = agent.solveMaze(noIterations)
    performance.addTrialRecords(iterationPerformance)
  
  with open("MultiPredResults.json", "w") as resultsFile:
    resultsFile.write(json.dumps(performance.toJSON()))

if __name__ == "__main__":
  main()
