from nupic.frameworks.opf.modelfactory import ModelFactory
from random import choice
import model_params

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

NoIterations = 30000
             

def main():
  model = createModel()
  for iteration in range(NoIterations):
    doIteration(iteration, model)


def doIteration(iteration, model):
  processSequence(model, iteration, getSequence())


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
    return "B"
  elif state == "B":
    return "C"
  elif state == "C":
    return choice(["B", "K", "G"])
  elif state == "K":
    return choice(["C","B"])
  elif state == "G":
    return "E"
  else:
    raise Exception("Unrecognized state {}".format(state))

def getRewardFor(state, keyVisited):
  if state == "G":
    return 1 if keyVisited else -1
  else:
     return 0


def processSequence(model, iteration, sequence):
  for position in sequence:
    processPosition(model, iteration, position)
  model.resetSequenceStates()


def processPosition(model, iteration, position):
  modelInput = dict(zip(Headers, position))
  predictedReward = predictReward(model, modelInput)
  print "At iteration {}: position {} -> prediction {}".format(iteration, position, predictedReward)


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
