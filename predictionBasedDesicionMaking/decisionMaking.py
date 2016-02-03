from Maze import Maze
from HTMModel import HTMModel
from Agent import Agent
from QLearningModel import QLearningModel
import json
import matplotlib
matplotlib.use("Agg") # Force matplotlib to not use any Xwindows backend
import matplotlib.pyplot as plt

ITERATIONS_PER_TRIAL = 500
MAZE_EXTRA_STATES = 1
No_TRIALS = 10

TESTING_ITERATIONS = ITERATIONS_PER_TRIAL
TRAINING_ITERATIONS = 0

if __name__ == "__main__":
  mazes = [MAZE_EXTRA_STATES] * No_TRIALS
 
  severalMazesPerformance = []
  for mazeLength in mazes:
    maze = Maze(mazeLength)
    #tdModel = QLearningModel(maze.AllStates)
    tdModel = HTMModel(maze.AllStates)
    tdAgent = Agent(maze, tdModel, TRAINING_ITERATIONS, TESTING_ITERATIONS)
    tdPerformance = tdAgent.run()
    severalMazesPerformance.append(tdPerformance)

  #Convert to a more usable format
  results = []
  avgRewards = []
  avgSteps = []
  for iterationNo in range(ITERATIONS_PER_TRIAL):
    stepsToSolution = []
    accumulatedRewards = []
    for trialNo in range(No_TRIALS):
      stepToSolution = severalMazesPerformance[trialNo][1][iterationNo][1][0]
      accumulatedReward = severalMazesPerformance[trialNo][1][iterationNo][1][1]
      stepsToSolution.append(stepToSolution)
      accumulatedRewards.append(accumulatedReward)
    results.append({"IterationNo": iterationNo, 
		    "StepsToSolution": stepsToSolution,
		    "AccumulatedRewards": accumulatedRewards})
    avgRewards.append(sum(accumulatedRewards)/len(accumulatedRewards))
    avgSteps.append(sum(stepsToSolution)/len(stepsToSolution))

  with open("results", "w") as file:
    file.write(json.dumps(results))

  #create plot
  plt.plot(range(len(avgRewards)), avgRewards)
  plt.axis([0, len(avgRewards), -2, 2])
  plt.savefig("accRew.png")
 


#    htmModel = HTMModel(maze.AllStates)
#    htmAgent = Agent(maze, htmModel, TRAINING_ITERATIONS, TESTING_ITERATIONS)
#    print ">>change agent"
#    htmPerformance = htmAgent.run()
#    print "htmPerformance"
#    print htmPerformance
