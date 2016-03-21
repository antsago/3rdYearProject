#!/usr/bin/python
from src import AgentFactory, Experiment
import sys
import traceback

if __name__ == "__main__":
    try:
      if len(sys.argv) != 6:
        raise Exception("Wrong number of arguments, see usage")
      expType = sys.argv[1]
      problemName = sys.argv[2]
      modelName = sys.argv[3]
      noTrials = int(sys.argv[4])
      noIterations = int(sys.argv[5])

      experimentName = "{}-{}-{}.json".format(expType, modelName, problemName)

      agentFactory = AgentFactory(expType, problemName, modelName)
      experiment = Experiment(agentFactory)

      experiment.run(noIterations, noTrials)
      experiment.saveResults(experimentName)
      
      print "Results saved in file {}".format(experimentName)
    except:
      print traceback.format_exc()
      print "Usage: runExperiment {}|{} {}|{}|{} {}|{} noTrials noIterations".format(AgentFactory.PRED_TYPE,
                                                                                     AgentFactory.BEH_TYPE,
                                                                                     AgentFactory.BASIC_PBM,
                                                                                     AgentFactory.SEC_ORDER_PBM,
                                                                                     AgentFactory.MULTI_STEP_PBM,
                                                                                     AgentFactory.HTM_MODEL,
                                                                                     AgentFactory.Q_MODEL)
