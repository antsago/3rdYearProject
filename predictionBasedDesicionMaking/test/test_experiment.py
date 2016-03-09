from mock import MagicMock
from unittest import TestCase
from src import Experiment, Agent, PerformanceRecord

class TestExperiment(TestCase):

  def test_whenRunSolveMazeIsCalledNoTrialsTimes(self):
    noTrials = 2
    noIterations = 2

    mockedAgent = Agent(None, None, None)
    performance = {iteration: PerformanceRecord([0]) for iteration in range(noIterations)}
    mockedAgent.solveMaze = MagicMock(return_value=performance)
    experiment = Experiment(mockedAgent)
    
    experiment.run(1, noTrials)

    mockedAgent.solveMaze.assert_called(noTrials)

