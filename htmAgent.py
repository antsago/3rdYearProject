__author__ = 'Thomas Rueckstiess, ruecksti@in.tum.de'

from pybrain.rl.agents.agent import Agent
from scipy import zeros
from nupic.frameworks.opf.modelfactory import ModelFactory
import model_params
from random import choice, uniform, random
from math import fabs

class HTMAgent(Agent):
    """ Agent that uses an HTM sequential memory to decide its actions"""

    logging = True

    lastobs = None
    lastaction = None
    lastreward = None


    def __init__(self, **kwargs):
        self.setArgs(**kwargs)
        self.htmModel = ModelFactory.create(model_params.MODEL_PARAMS)
        self.htmModel.enableInference({'predictedField': 'reward'})
        self.lastreward = 0


    def integrateObservation(self, obs):
        self.lastobs = obs


    def getPredictions(self, possibleActions):
        self.htmModel.disableLearning()
        modelInput = \
        {
            'reward': self.lastreward,
            'nextAction': None,
            'state': self.lastobs[0],
        }
        predictions = [None] * 4
        for actionNo, action in enumerate(possibleActions):
            modelInput["nextAction"] = action
            result = self.htmModel.run(modelInput)
            predictions[actionNo] = result.inferences["multiStepBestPredictions"][1]

        self.htmModel.enableLearning()
        return predictions
        

    def getAction(self):
        possibleActions = [0,1,2,3]
        predictions = self.getPredictions(possibleActions)
        print predictions
        nextAction = self.selectAction(predictions)
        self.takeAction(nextAction)
        return [nextAction]

    def selectAction(self, predictedRewards):
        #minReward = fabs(min(predictedRewards))
        #totalPredictedRewards = sum(predictedReward+minReward for action, predictedReward in enumerate(predictedRewards))
        #rand = uniform(minReward, totalPredictedRewards)
        #upto = minReward
        #for action, predictedReward in enumerate(predictedRewards):
        #   if upto + predictedReward >= rand:
        #      return action
        #   upto += predictedReward
        #assert False, "Shouldn't get here"
        i = random()
        if i <= 0.5:
            return choice(range(len(predictedRewards)))
        else:
            maxPrediction = max(predictedRewards)
            bestActions = [i for i, j in enumerate(predictedRewards) if j == maxPrediction]
            return choice(bestActions)


    def takeAction(self, action):
        modelInput = \
        {
            'reward': self.lastreward,
            'nextAction': action,
            'state': self.lastobs[0],
        }
        self.htmModel.run(modelInput)
        


    def giveReward(self, r):
        self.lastreward

    def newEpisode(self):
        pass


    def reset(self):
        """ Clear the history of the agent. """
        self.lastobs = None
        self.lastaction = None
        self.lastreward = None
