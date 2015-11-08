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


def createModel():
  return ModelFactory.create(model_params.MODEL_PARAMS)



def runHotgym():
  model = createModel()
  model.enableInference({'predictedField': 'reward'})
  with open (_INPUT_FILE_PATH) as fin:
    reader = csv.reader(fin)
    headers = reader.next()
    reader.next()
    reader.next()
    previousPrediction = 0
    for rerun in range(30000):
        noErrors = 0
        for i, record in enumerate(reader, start=1):
          modelInput = dict(zip(headers, record))
          modelInput["reward"] = float(modelInput["reward"])

          result = model.run(modelInput)

          isTruePrediction = previousPrediction==modelInput["reward"]
          #_LOGGER.info("%s prediction: Predicted %i, real was %i", isTruePrediction, previousPrediction, modelInput["reward"])
          if not isTruePrediction:
              noErrors += 1
          previousPrediction = result.inferences["multiStepBestPredictions"][1]
        _LOGGER.info(">>>> Had %i errors at iteration %i", noErrors, rerun)
        fin.seek(0)
        reader.next()
	reader.next()
        reader.next()



if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  runHotgym()
