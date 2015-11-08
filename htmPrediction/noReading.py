#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

"""A simple client to create a CLA model for hotgym."""

import csv
import datetime
import logging

from pkg_resources import resource_filename

from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.predictionmetricsmanager import MetricsManager

import model_params

_LOGGER = logging.getLogger(__name__)

_INPUT_FILE_PATH = "rec-center-hourly.csv"

ACTIONS = ["North", "South", "West", "East"]
REWARDS = [0.0, 0.0, 0.0, 1.0]

def createModel():
  return ModelFactory.create(model_params.MODEL_PARAMS)


def doIteration(rewardForPreviousAction):
  action = chooseNextAction()
  modelInput = createInput(action, rewardForPreviousAction)
  predictedReward = predictReward(modelInput)
  actualReward = getRewardForAction(action)
  print predictedReward == actualReward
  rewardForPreviousAction = actualReward

def runHotgym():
  model = createModel()
  model.enableInference({'predictedField': 'reward'})
  previousPrediction = 0
  for rerun in range(450):
      noErrors = 0
      for i in range(4):
        modelInput = createInput(i)
        nextPrediction = runPrediction(model, modelInput)
        isTruePrediction = previousPrediction==modelInput["reward"]
        _LOGGER.info("%s prediction: Predicted %i, real was %i", isTruePrediction, previousPrediction, modelInput["reward"])
        if not isTruePrediction:
            noErrors += 1
        previousPrediction = nextPrediction
      _LOGGER.info(">>>> Had %i errors at iteration %i", noErrors, rerun)


def createInput(iteration):
    currentStage = iteration % len(ACTIONS)
    nextStage = (iteration+1) % len(ACTIONS)
    modelInput = \
    {
       "reward": REWARDS[currentStage],
       "nextAction": ACTIONS[nextStage],
       "state": 0
    }
    return modelInput


def runPrediction(model, modelInput):
    result = model.run(modelInput)
    predictedReward = result.inferences["multiStepBestPredictions"][1]
    return predictedReward


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  runHotgym()
