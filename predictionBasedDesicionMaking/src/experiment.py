from src import Agent, PerformanceResult
import json

class Experiment():

  def __init__(self, agent):
    self.agent = agent

  def run(self, noIterations, noTrials):
    self.results = PerformanceResult()
    for trial in range(noTrials):
      iterationPerformance = self.agent.solveMaze(noIterations)
      self.results.addTrialRecords(iterationPerformance)
    return self.results
  
  def saveResults(self, name):
    with open(name, "w") as resultsFile:
      resultsFile.write(json.dumps(self.results.toJSON()))

