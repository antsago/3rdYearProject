from mock import MagicMock
from unittest import TestCase
from src import Experiment, AgentFactory, PerformanceRecord, Agent

class TestExperiment(TestCase):

  def test_whenRunSolveMazeIsCalledNoTrialsTimes(self):
    noTrials = 2
    noIterations = 2

    performance = {iteration: PerformanceRecord([0]) for iteration in range(noIterations)}
    mockedAgent = Agent(None, None, None)
    mockedAgent.solveMaze = MagicMock(return_value=performance)
    mockedAgentFactory = AgentFactory(None,None,None)
    mockedAgentFactory.createAgent = MagicMock(return_value=mockedAgent)
    experiment = Experiment(mockedAgentFactory)
    
    experiment.run(1, noTrials)

    mockedAgent.solveMaze.assert_called(noTrials)

