from src import SecondOrderImmediateProblem, FirstOrderImmediateProblem, HTMModel, Agent, QLearningModel, PerformanceResult
import json

def main():
  noTrials = 1
  noIterations = 1500

  performance = PerformanceResult()
  for trial in range(noTrials):
    maze = SecondOrderImmediateProblem()#FirstOrderImmediateProblem()
    model =  HTMModel(maze.AllStates)#QLearningModel(maze.AllStates)
    agent = Agent(maze, model, degradeEpsilon = True)
    iterationPerformance = agent.solveMaze(noIterations)
    performance.addTrialRecords(iterationPerformance)
    with open("htmSecondImBehResults{}.json".format(trial), "w") as resultsFile:
      resultsFile.write(json.dumps(performance.toJSON()))
  
#  print "\n{}".format(json.dumps(performance.toJSON(), sort_keys=True,
#                  indent=4, separators=(',', ': ')))
#  print "\n{}".format(model.valueTable)
  with open("htmSecondImBehResults.json", "w") as resultsFile:
    resultsFile.write(json.dumps(performance.toJSON()))

if __name__ == "__main__":
  main()
