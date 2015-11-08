from nupic.frameworks.opf.modelfactory import ModelFactory
from random import choice
import model_params
import pickle

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


PossibleActionsFrom = { "S": ["C"],
                        "C": ["K", "G"],
                        "K": ["C"],
                        "G": ["E"],
                      }
            


TrainingIterations = 500
TestIterations = 500

ExtraDataPath = "/home/docker/testSequencePrediction/ExtraSerializedData"
             

def main():
  model = createModel()
  maze = getSequence
  trainModel(model, maze)
  print "### End training, start testing ###"
  testModel(model)


def testModel(model, noIterations = TestIterations):
  for iteration in range(noIterations):
    solveMaze(model, iteration)


def trainModel(model, maze, noIterations = TrainingIterations):
  for iteration in range(noIterations):
    processSequence(model, iteration, maze())


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
  return choice(PossibleActionsFrom[state])


def getRewardFor(state, keyVisited):
  if state == "G":
    return 1 if keyVisited else -1
  else:
     return 0


def solveMaze(model, iteration):
  currentState = "S"
  keyVisited = False
  while currentState != "G":
    nextPossibleStates = PossibleActionsFrom[currentState]
    reward = getRewardFor(currentState, keyVisited)
    predictedRewardsPerState = simulateMoves(currentState, nextPossibleStates, model, reward)
    nextState = bestNextState(predictedRewardsPerState)
    moveToState(nextState, model, currentState, reward)
    print "At iteration {} took moved to state {}. Predictions: {}".format(iteration, nextState, predictedRewardsPerState)
    currentState = nextState
    if currentState == "K":
      keyVisited = True

  model.resetSequenceStates()


def bestNextState(predictedRewards):
  bestReward = max(predictedRewards.values())
  return choice([state for state in predictedRewards.keys() if predictedRewards[state] == bestReward])

def processSequence(model, iteration, sequence):
  for position in sequence:
    processPosition(model, iteration, position)
  model.resetSequenceStates()


def processPosition(model, iteration, position):
  predictedReward = executePosition(position, model)
  print "At iteration {}: position {} -> prediction {}".format(iteration, position, predictedReward)


def simulateMoves(currentState, nextStates, model, reward):
  pickledModel = saveModel(model)
  return { nextState: simulateMove(nextState, currentState, pickledModel, reward) for nextState in nextStates } 


def saveModel(model):
  pickledModel = pickle.dumps(model)
  model._serializeExtraData(ExtraDataPath)
  return pickledModel


def loadModel(pickledModel):
  model = pickle.loads(pickledModel)
  model._deSerializeExtraData(ExtraDataPath)
  return model


def simulateMove(nextState, currentState, pickledModel, reward):
  model = loadModel(pickledModel)
  return moveToState(nextState, model, currentState, reward)


def moveToState(nextState, model, currentState, reward):
  position = [currentState, nextState, reward]
  return executePosition(position, model)


def createModel():
  parameters = model_params.MODEL_PARAMS
  parameters["modelParams"]["sensorParams"]["encoders"] = Encoders
  model = ModelFactory.create(parameters)
  model.enableInference({'predictedField': 'reward'})
  return model


def executePosition(position, model):
  modelInput = createInput(position)
  return executeInput(model, modelInput)


def executeInput(model, modelInput):
  result = model.run(modelInput)
  return result.inferences["multiStepBestPredictions"][1]

 
def createInput(position):
  return dict(zip(Headers, position))


if __name__ == "__main__":
  main()
