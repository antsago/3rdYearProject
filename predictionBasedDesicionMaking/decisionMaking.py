from src import SecondOrderImmediateProblem, FirstOrderImmediateProblem, HTMModel, Agent, QLearningModel, ConfusionMatrix
import json

#MAZE_EXTRA_STATES = 1
#No_TRIALS = 10
#
#TESTING_ITERATIONS = 1
#TRAINING_ITERATIONS = range(200, 4001, 100)
#

def main():
  noTrials = 100
  trainingRange = range(0, 100, 10) + range(100, 1001, 100)
  
  matrixPerformance = {noTrainingIterations:calculateConfusionMatrix(noTrials, noTrainingIterations)
                       for noTrainingIterations in trainingRange}

  with open("sequencePredictionResults", "w") as resultsFile:
    resultsFile.write(json.dumps(matrixPerformance))

def calculateConfusionMatrix(noTrials, noTrainingIterations):
  confusionMatrix = ConfusionMatrix(FirstOrderImmediateProblem.POSSIBLE_REWARDS)

  for trial in range(noTrials):
    maze = FirstOrderImmediateProblem()
    model = HTMModel(maze.AllStates)
    agent = Agent(maze, model, 0)
    agent.solveMaze(noTrainingIterations)
    tempConfMatrix = agent.solveMaze(1)
    confusionMatrix.merge(tempConfMatrix)
  
  return confusionMatrix.toJSON()
  


#
#
#
#
#  performancePerTrain = []
#  
#  for noTrainIterations in TRAINING_ITERATIONS:
#
#    severalMazesPerformance = []
#    for trial in range(No_TRIALS):
#      maze = Maze()
#      #tdModel = QLearningModel(maze.AllStates)
#      tdModel = HTMModel(maze.AllStates)
#      tdAgent = Agent(maze, tdModel, noTrainIterations, TESTING_ITERATIONS)
#      tdPerformance = tdAgent.run()
#      severalMazesPerformance.append(tdPerformance)
#
#    #Convert to a more usable format
#    results = []
#    avgRewards = []
#    avgSteps = []
#    for iterationNo in range(TESTING_ITERATIONS):
#      stepsToSolution = []
#      accumulatedRewards = []
#      for trialNo in range(No_TRIALS):
#        stepToSolution = severalMazesPerformance[trialNo][1][iterationNo][1][0]
#        accumulatedReward = severalMazesPerformance[trialNo][1][iterationNo][1][1]
#        stepsToSolution.append(stepToSolution)
#        accumulatedRewards.append(accumulatedReward)
#      results.append({"IterationNo": iterationNo, 
#  		    "StepsToSolution": stepsToSolution,
#  		    "AccumulatedRewards": accumulatedRewards})
#      avgRewards.append(sum(accumulatedRewards)/len(accumulatedRewards))
#      avgSteps.append(sum(stepsToSolution)/len(stepsToSolution))
#
#    performancePerTrain.append({"NoTrainIterations": noTrainIterations,
#                                "StepsToSolution": sum(avgSteps)/len(avgSteps),
#                                "AccumulatedRewards": sum(avgRewards)/len(avgRewards)})
#
#  with open("resultsPerTrain", "w") as file:
#    file.write(json.dumps(performancePerTrain))
#
if __name__ == "__main__":
  main()
