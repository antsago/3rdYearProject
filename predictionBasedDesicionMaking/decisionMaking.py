from Maze import Maze
from HTMModel import HTMModel
from Agent import Agent
from QLearningModel import QLearningModel
import json
import matplotlib
matplotlib.use("Agg") # Force matplotlib to not use any Xwindows backend
import matplotlib.pyplot as plt

MAZE_EXTRA_STATES = 1
No_TRIALS = 10

TESTING_ITERATIONS = 1
TRAINING_ITERATIONS = range(200, 4001, 100)

if __name__ == "__main__":
 
  performancePerTrain = []
  
  for noTrainIterations in TRAINING_ITERATIONS:

    severalMazesPerformance = []
    for trial in range(No_TRIALS):
      maze = Maze()
      #tdModel = QLearningModel(maze.AllStates)
      tdModel = HTMModel(maze.AllStates)
      tdAgent = Agent(maze, tdModel, noTrainIterations, TESTING_ITERATIONS)
      tdPerformance = tdAgent.run()
      severalMazesPerformance.append(tdPerformance)

    #Convert to a more usable format
    results = []
    avgRewards = []
    avgSteps = []
    for iterationNo in range(TESTING_ITERATIONS):
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

#    with open("results{}".format(noTrainIterations), "w") as file:
#      file.write(json.dumps(results))
    
    
    performancePerTrain.append({"NoTrainIterations": noTrainIterations,
                                "StepsToSolution": sum(avgSteps)/len(avgSteps),
                                "AccumulatedRewards": sum(avgRewards)/len(avgRewards)})

  with open("resultsPerTrain", "w") as file:
    file.write(json.dumps(performancePerTrain))
    

#  #create plot
#  plt.plot(range(len(avgRewards)), avgRewards)
#  plt.axis([0, len(avgRewards), -2, 2])
#  plt.savefig("accRew.png")
 


#    htmModel = HTMModel(maze.AllStates)
#    htmAgent = Agent(maze, htmModel, TRAINING_ITERATIONS, TESTING_ITERATIONS)
#    print ">>change agent"
#    htmPerformance = htmAgent.run()
#    print "htmPerformance"
#    print htmPerformance
