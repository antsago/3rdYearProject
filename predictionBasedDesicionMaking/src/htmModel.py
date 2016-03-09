from random import choice

class HTMModel:
  Headers = ["currentState", "nextState", "reward"]
  ExtraDataPath = "/tmp/htmSerialization"

  def __init__(self, htmModule):
    self.htm = htmModule

  def problemFinished(self):
    self.htm.resetSequenceStates()
  
  def makeMove(self, currentState, currentStateReward, nextState):
    pred = self._moveToState(self.htm, currentState, currentStateReward, nextState) 
    return pred

  def predictRewards(self, currentState, currentStateReward, nextPossibleStates):
    pickledModel = self._saveModel()
    return { nextState: self._simulateMove(pickledModel, currentState, currentStateReward, nextState) for nextState in nextPossibleStates } 
  
  def _simulateMove(self, pickledModel, currentState, currentStateReward, nextState):
    model = self._loadModel(pickledModel)
    return self._moveToState(model, currentState, currentStateReward, nextState)

  def _moveToState(self, model, currentState, currentStateReward, nextState):
    position = [currentState, nextState, currentStateReward]
    return self._executePosition(position, model)
  
  def _saveModel(self):
   self.htm.save(self.ExtraDataPath)

  def _loadModel(self, pickledModel):
    return self.htm.load(self.ExtraDataPath)

  def _executePosition(self, position, model):
    modelInput = self._createInput(position)
    return self._executeInput(model, modelInput)
  
  def _executeInput(self, model, modelInput):
    result = model.run(modelInput)
    return result.inferences["multiStepBestPredictions"][1]
   
  def _createInput(self, position):
    return dict(zip(self.Headers, position))
