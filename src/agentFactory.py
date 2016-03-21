from src import SecondOrderImmediateProblem, FirstOrderImmediateProblem, HTMModel, QLearningModel, MultiStepProblem, HTMModuleFactory, Agent

class AgentFactory():
  BASIC_PBM = "Basic"
  SEC_ORDER_PBM = "SecondOrder"
  MULTI_STEP_PBM = "MultiStep"
 
  HTM_MODEL = "HTM"
  Q_MODEL = "QLearning"
  
  PRED_TYPE = "Prediction"
  BEH_TYPE = "Behaviour"

  def __init__(self, experimentType, problem, model):
    self.problemName = problem
    self.experimentType = experimentType
    self.modelName = model

  def createAgent(self):
    problem = self.parseProblem(self.problemName)
    model = self.parseModel(problem.AllStates, self.modelName)
    epsilonPolicy = self.parseEpsilonPolicy(self.experimentType, self.problemName, self.modelName)
    return Agent(problem, model, epsilonPolicy)

  def parseProblem(self, problemName):
    if problemName == self.BASIC_PBM:
      problem = FirstOrderImmediateProblem()
    elif problemName == self.SEC_ORDER_PBM:
      problem = SecondOrderImmediateProblem()
    elif problemName == self.MULTI_STEP_PBM:
      problem = MultiStepProblem()
    else:
      raise ValueError("Problem {} not recognized", problem)
    return problem
   
  def parseModel(self, problemStates, modelName):
    if modelName == self.HTM_MODEL:
      module = HTMModuleFactory().createModule(problemStates)
      model = HTMModel(module)
    elif modelName == self.Q_MODEL:
      model = QLearningModel(problemStates)
    else:
      raise ValueError("Model {} not recognized", model)
    return model

  def parseEpsilonPolicy(self, experimentType, problemName, modelName):
    if experimentType == self.PRED_TYPE:
      epsilonPolicy = lambda iteration: 1.0
    elif experimentType != self.BEH_TYPE:
      raise ValueError("Experiment type {} not recognized", experimentType)
    elif modelName == self.Q_MODEL or (modelName == self.HTM_MODEL and (problemName == self.BASIC_PBM or problemName == self.MULTI_STEP_PBM)):
      epsilonPolicy = lambda iteration: 1.0/iteration
    elif modelName == self.HTM_MODEL and problemName == self.SEC_ORDER_PBM:
      epsilonPolicy = lambda iteration: min(0.9, 100.0/iteration)
    else:
      raise ValueError("Combination of type: {},  problem: {} and model: {} not recognized", experimentType, problemName, modelName)
    return epsilonPolicy
  
