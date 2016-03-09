#!/usr/bin/python
from src import ExperimentFactory
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

      factory = ExperimentFactory()
      experiment = factory.createExperiment(expType, problemName, modelName)

      experiment.run(noIterations, noTrials)
      experiment.saveResults(experimentName)
      
      print "Results saved in file {}".format(experimentName)
    except:
      print traceback.format_exc()
      print "Usage: runExperiment {}|{} {}|{}|{} {}|{} noTrials noIterations".format(ExperimentFactory.PRED_TYPE,
                                                                                     ExperimentFactory.BEH_TYPE,
                                                                                     ExperimentFactory.BASIC_PBM,
                                                                                     ExperimentFactory.SEC_ORDER_PBM,
                                                                                     ExperimentFactory.MULTI_STEP_PBM,
                                                                                     ExperimentFactory.HTM_MODEL,
                                                                                     ExperimentFactory.Q_MODEL)
