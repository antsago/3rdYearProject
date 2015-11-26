from nupic.frameworks.opf.modelfactory import ModelFactory
import model_params
import pickle

class HTMModel:
  Headers = ["currentState", "nextState", "reward"]
  Encoders = \
  {
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

  ExtraDataPath = "/home/docker/testSequencePrediction/ExtraSerializedData"

  def __init__(self, listOfStates):
    moduleParameters = self._getModuleParameters(listOfStates)
    self.htm = self._createHTMModule(moduleParameters)

  def predictRewards(self, currentState, currentStateReward, nextPossibleStates):
    pickledModel = self._saveModel()
    return { nextState: self._simulateMove(pickledModel, currentState, currentStateReward, nextState) for nextState in nextPossibleStates } 
  
  def makeMove(self, currentState, currentStateReward, nextState):
    self._moveToState(self.htm, currentState, currentStateReward, nextState) 

  def problemFinished(self):
    self.htm.resetSequenceStates()
  
  def _createHTMModule(self, moduleParameters):
    model = ModelFactory.create(moduleParameters)
    model.enableInference({'predictedField': 'reward'})
    return model

  def _getModuleParameters(self, listOfStates):
    parameters = model_params.MODEL_PARAMS
    self.Encoders["currentState"]["categoryList"] = listOfStates
    self.Encoders["nextState"]["categoryList"] = listOfStates
    parameters["modelParams"]["sensorParams"]["encoders"] = self.Encoders
    return parameters

  def _simulateMove(self, pickledModel, currentState, currentStateReward, nextState):
    model = self._loadModel(pickledModel)
    return self._moveToState(model, currentState, currentStateReward, nextState)
  
  def _moveToState(self, model, currentState, currentStateReward, nextState):
    position = [currentState, nextState, currentStateReward]
    return self._executePosition(position, model)
  
  def _saveModel(self):
    pickledModel = pickle.dumps(self.htm)
    self.htm._serializeExtraData(self.ExtraDataPath)
    return pickledModel

  def _loadModel(self, pickledModel):
    model = pickle.loads(pickledModel)
    model._deSerializeExtraData(self.ExtraDataPath)
    return model

  def _executePosition(self, position, model):
    modelInput = self._createInput(position)
    return self._executeInput(model, modelInput)
  
  def _executeInput(self, model, modelInput):
    result = model.run(modelInput)
    return result.inferences["multiStepBestPredictions"][1]
   
  def _createInput(self, position):
    return dict(zip(self.Headers, position))
