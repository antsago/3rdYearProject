from mock import MagicMock
from unittest import TestCase
from src import HTMModel, HTMModuleFactory

class TestHTMModel(TestCase):

  def test_whenProblemFinishedResetSequenceIsCalled(self):
    mockedModule = HTMModuleFactory().createModule(["A"])
    mockedModule.resetSequenceStates = MagicMock()
    model = HTMModel(mockedModule)
    
    model.problemFinished()

    mockedModule.resetSequenceStates.resetSequenceStates.assert_called_once()

  def test_whenMakeAMoveSequenceIsInvoked(self):
    mockedModule = HTMModuleFactory().createModule(["A"])
    mockedModule.run = MagicMock()
    model = HTMModel(mockedModule)
    
    model.makeMove("A", 0, "A")

    mockedModule.run.assert_called_once()

  def test_whenPredictingRewardsModuleIsSaveAndLoadedForEachPossibleState(self):
    mockedModule = HTMModuleFactory().createModule(["A", "B"])
    mockedModule.run = MagicMock()
    mockedModule.load = MagicMock()
    mockedModule.save = MagicMock()
    model = HTMModel(mockedModule)
    
    model.predictRewards("A", 0, ["A", "B"])

    mockedModule.run.assert_called_twice()
    mockedModule.save.assert_called_once()
    mockedModule.load.assert_called_twice()
