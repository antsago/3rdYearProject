from nupic.frameworks.opf.modelfactory import ModelFactory
from random import choice
import model_params
import json

KeyedSequence = [["S", "C", 0],
                 ["C", "K", 0],
                 ["K", "C", 0],
                 ["C", "G", 0],
                 ["G", "E", 1]]

NoKeySequence = [["S", "C", 0],
                 ["C", "G", 0],
                 ["G", "E", -1]]

Headers = ["currentState", "nextState", "reward"]
Encoders = {
             'currentState': {
                 'fieldname':"currentState",
                 'name':'currentState',
                 'type':'CategoryEncoder',
                 'categoryList':["B", "S","C","K","G", "E"],
                 'w':21
              },
             'nextState': {
                 'fieldname':"nextState",
                 'name':'nextState',
                 'type':'CategoryEncoder',
                 'categoryList':["B", "S","C","K","G", "E"],
                 'w':21
              },
             'reward': {
                 'fieldname':"reward",
                 'name':'reward',
                 'type':'ScalarEncoder',
                 'maxval':1,
                 'minval':-1,
                 'w':21,
                 'resolution':1,
              },
           }


def main():
  iterationStages = range(0,100, 10) + range(100, 1000, 100) + range(1000, 10001, 1000)
  results = []
  for noIterations in iterationStages:
    model = createModel()
    #outer loop, real/true reward, inner is predicted reward
    confusionMatrix = {0:{0:0,1:0,-1:0}, 1:{0:0,1:0,-1:0}, -1:{0:0,1:0,-1:0}}
 
    for iteration in range(noIterations):
      processSequence(model, iteration, getSequence(), confusionMatrix)

    results.append({ 
      "noIterations": noIterations,
      "confusionMatrix": confusionMatrix,
      "accuracy": calculateAccuracy(confusionMatrix),
      "precision0": calculatePrecision(0, confusionMatrix),
      "recall0": calculateRecall(0, confusionMatrix),
      "precision1": calculatePrecision(1, confusionMatrix),
      "recall1": calculateRecall(1, confusionMatrix),
      "precision-1": calculatePrecision(-1, confusionMatrix),
      "recall-1": calculateRecall(-1, confusionMatrix),})

  with open("results", "w") as file:
    file.write(json.dumps(results))

def calculateAccuracy(confusionMatrix):
  predictedPopulation = sum([confusionMatrix[0][0], confusionMatrix[1][1], confusionMatrix[-1][-1]])
  totalPopulation = sum([sum([confusionMatrix[trueValue][predictedValue] for predictedValue in confusionMatrix[trueValue]]) for trueValue in confusionMatrix])
  return 100 * predictedPopulation / totalPopulation if totalPopulation > 0 else 0

def calculateRecall(no, confusionMatrix):
  classPopulation = sum([confusionMatrix[no][predictedValue] for predictedValue in confusionMatrix[no]])
  return 100 * confusionMatrix[no][no] / classPopulation if classPopulation > 0 else 0 

def calculatePrecision(no, confusionMatrix):
  noPredictions = sum([confusionMatrix[trueValue][no] for trueValue in confusionMatrix])
  return 100 * confusionMatrix[no][no] / noPredictions if noPredictions > 0 else 0 

def getSequence():
  currentState = "S"
  keyVisited = False
  while currentState != "E":
    nextState = getNextStateFrom(currentState)
    reward = getRewardFor(currentState, keyVisited)
    yield [currentState, nextState, reward]
   
    currentState = nextState
    if currentState == "K":
      keyVisited = True


def getNextStateFrom(state):
  if state == "S":
    return "C"
  elif state == "C":
    return choice(["K", "G"])
  elif state == "K":
    return "C"#choice(["C","B"])
  elif state == "G":
    return "E"
  else:
    raise Exception("Unrecognized state {}".format(state))

def getRewardFor(state, keyVisited):
  if state == "G":
    return 1# if keyVisited else -1
  else:
     return 0


def processSequence(model, iteration, sequence, confusionMatrix):
  predictedReward = 0
  for position in sequence:
    currentReward = position[2]
    confusionMatrix[currentReward][predictedReward] += 1
    predictedReward = processPosition(model, iteration, position)
    
  model.resetSequenceStates()


def processPosition(model, iteration, position):
  modelInput = dict(zip(Headers, position))
  predictedReward = predictReward(model, modelInput)
  print "At iteration {}: position {} -> prediction {}".format(iteration, position, predictedReward)
  return predictedReward


def createModel():
  parameters = model_params.MODEL_PARAMS
  parameters["modelParams"]["sensorParams"]["encoders"] = Encoders
  model = ModelFactory.create(parameters)
  model.enableInference({'predictedField': 'reward'})
  return model


def predictReward(model, modelInput):
  result = model.run(modelInput)
  return result.inferences["multiStepBestPredictions"][1]

 
if __name__ == "__main__":
  main()
