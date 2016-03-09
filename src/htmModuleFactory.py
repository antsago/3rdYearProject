from nupic.frameworks.opf.modelfactory import ModelFactory
import htmModelParams
 
class HTMModuleFactory():
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

  def createModule(self, listOfStates):
    moduleParameters = self._getModuleParameters(listOfStates)
    model = ModelFactory.create(moduleParameters)
    model.enableInference({'predictedField': 'reward'})
    return model

  def _getModuleParameters(self, listOfStates):
    parameters = htmModelParams.MODEL_PARAMS
    self.Encoders["currentState"]["categoryList"] = listOfStates
    self.Encoders["nextState"]["categoryList"] = listOfStates
    parameters["modelParams"]["sensorParams"]["encoders"] = self.Encoders
    return parameters
