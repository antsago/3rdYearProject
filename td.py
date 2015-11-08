#!/usr/bin/env python
__author__ = 'Thomas Rueckstiess, ruecksti@in.tum.de'

""" This example demonstrates how to use the discrete Temporal Difference
Reinforcement Learning algorithms (SARSA, Q, Q(lambda)) in a classical
fully observable MDP maze task. The goal point is the top right free
field. """

from scipy import * #@UnusedWildImport

from htmAgent import HTMAgent

from pybrain.rl.environments.mazes import Maze, MDPMazeTask, TrivialMaze
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q, QLambda, SARSA #@UnusedImport
from pybrain.rl.explorers import BoltzmannExplorer #@UnusedImport
from pybrain.rl.experiments import Experiment


def doInteraction():
        """ Give the observation to the agent, takes its resulting action and returns
            it to the task. Then gives the reward to the agent again and returns it.
        """
        observation = task.getObservation()
        agent.integrateObservation(observation)

        action = agent.getAction()
        task.performAction(action[0])

        reward = task.getReward()
        agent.giveReward(reward)
       
        print "Took action {} with reward {}".format(action, reward)

        return reward == 1


# create the maze with walls (1)
envmatrix = array([[1, 1, 1, 1, 1, 1],
                   [1, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 1],
                   [1, 1, 1, 1, 1, 1]])

env = Maze(envmatrix, (2, 4))

# create task
#task = MDPMazeTask(env)
task = TrivialMaze()

# create value table and initialize with ones
table = ActionValueTable(81, 4)
table.initialize(1.)

# create agent with controller and learner - use SARSA(), Q() or QLambda() here
learner = SARSA()

# standard exploration is e-greedy, but a different type can be chosen as well
# learner.explorer = BoltzmannExplorer()

# create agent
agent = HTMAgent() # LearningAgent(table, learner)

# create experiment
experiment = Experiment(task, agent)

for experiment in range(200000):
    i = 0
    while True:
        solved = doInteraction()
        if solved:
            print "Solved at iteration %i" % i
            break
        i += 1 

