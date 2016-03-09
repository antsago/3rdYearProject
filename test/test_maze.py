import unittest
from src import Maze

class TestMaze(unittest.TestCase):

  def test_whenInitializedCurrentStateIsStart(self):
    maze = Maze()
    self.assertEqual(maze.START_STATE, maze.currentState)

  def test_whenInitializedKeyIsNotVisited(self):
    maze = Maze()
    self.assertFalse(maze.keyVisited)

  def test_whenMoveToKeyStateKeyIsVisited(self):
    maze = Maze()
    maze.getPossibleActionsFrom = lambda s: maze.KEY_STATE
    maze.moveTo(maze.KEY_STATE)
    self.assertTrue(maze.keyVisited)

  def test_whenMoveToEndMazeIsFinished(self):
    maze = Maze()
    maze.getPossibleActionsFrom = lambda s: maze.END_STATE
    maze.moveTo(maze.END_STATE)
    self.assertFalse(maze.isNotFinished())

  def test_whenResetCurrentStateIsStart(self):
    maze = Maze()
    maze.getPossibleActionsFrom = lambda s: maze.END_STATE
    maze.moveTo(maze.END_STATE)

    maze.reset()
    self.assertEqual(maze.START_STATE, maze.currentState)

  def test_whenResetKeyIsNotVisited(self):
    maze = Maze()
    maze.getPossibleActionsFrom = lambda s: maze.KEY_STATE
    maze.moveTo(maze.KEY_STATE)

    maze.reset()
    self.assertFalse(maze.keyVisited)

  def test_whenMoveCurrentStateChanges(self):
    maze = Maze()
    maze.getPossibleActionsFrom = lambda s: maze.END_STATE
    maze.moveTo(maze.END_STATE)
    self.assertEqual(maze.END_STATE, maze.currentState)
