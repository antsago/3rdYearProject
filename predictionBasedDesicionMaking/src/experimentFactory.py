from src import SecondOrderImmediateProblem, FirstOrderImmediateProblem, HTMModel, QLearningModel, MultiStepProblem, Experiment

class ExperimentFactory():
  BASIC_PBM = "Basic"
  SEC_ORDER_PBM = "SecondOrder"
  MULTI_STEP_PBM = "MultiStep"
 
  HTM_MODEL = "HTM"
  Q_MODEL = "QLearning"
  
  PRED_TYPE = "Prediction"
  BEH_TYPE = "Behaviour"

  def createExperiment(self, experimentType, problem, model): 
    self.parseProblem(problem)
    self.parseModel(model)
    self.parseEpsilonPolicy(experimentType, problem, model)
    return Experiment(self.problem, self.model, self.epsilonPolicy)

  def parseProblem(self, problemName):
    if problemName == self.BASIC_PBM:
      self.problem = FirstOrderImmediateProblem()
    elif problemName == self.SEC_ORDER_PBM:
      self.problem = SecondOrderImmediateProblem()
    elif problemName == self.MULTI_STEP_PBM:
      self.problem = MultiStepProblem()
    else:
      raise ValueError("Problem {} not recognized", problem)
   
  def parseModel(self, modelName):
    if modelName == self.HTM_MODEL:
      self.model = HTMModel(self.problem.AllStates)
    elif modelName == self.Q_MODEL:
      self.model = QLearningModel(self.problem.AllStates)
    else:
      raise ValueError("Model {} not recognized", model)

  def parseEpsilonPolicy(self, experimentType, problemName, modelName):
    if experimentType == self.PRED_TYPE:
      self.epsilonPolicy = lambda iteration: 1.0
    elif experimentType != self.BEH_TYPE:
      raise ValueError("Experiment type {} not recognized", experimentType)
    elif modelName == self.Q_MODEL or (modelName == self.HTM_MODEL and (problemName == self.BASIC_PBM or problem == self.MULTI_STEP_PBM)):
      self.epsilonPolicy = lambda iteration: 1.0/iteration
    elif modelName == self.HTM_MODEL and problem == self.SEC_ORDER_PBM:
      self.epsilonPolicy = lambda iteration: min(0.9, 100.0/iteration)
    else:
      raise ValueError("Combination of type: {},  problem: {} and model: {} not recognized", experimentType, problemName, modelName)
  
