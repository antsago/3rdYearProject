__author__ = 'Thomas Rueckstiess, ruecksti@in.tum.de'

from nupic.frameworks.opf.modelfactory import ModelFactory
import model_params
from random import choice, uniform, random

htmModel = ModelFactory.create(model_params.MODEL_PARAMS)
htmModel.enableInference({'predictedField': 'reward'})

actions = [0,1,2,3]
rewards = [0,0,0,1]
 

def start():
    
    actualReward = 0
    
    while True:
        nextAction = choice([0,1,2,3])
        actualReward, predictedReward = doIteration(nextAction, actualReward)
        print "For action {} predicted {} -> real was {}".format(nextAction, predictedReward, actualReward)


def doIteration(lastReward, nextAction):
    modelInput = \
    {
        'reward': lastReward,
        'nextAction': nextAction,
        'state':0
    }
    result = htmModel.run(modelInput)
    
    predictedReward = result.inferences["multiStepBestPredictions"][1]
    actualReward = rewards[nextAction]
    return actualReward, predictedReward

if __name__ == "__main__":
    start()
