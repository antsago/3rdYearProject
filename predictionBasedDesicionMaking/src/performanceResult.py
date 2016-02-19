class PerformanceResult:
  
  def __init__(self):
    self.results = {}  

  def addTrialRecords(self, iterationPerformance):
    for iteration in iterationPerformance.keys():
      self.addRecord(iteration, iterationPerformance[iteration])

  def addRecord(self, iteration, record):
    if iteration not in self.results.keys():
      self.results[iteration] = {}
      self.results[iteration]["ConfusionMatrix"] = record.confusionMatrix
      self.results[iteration]["AccumulatedReward"] = [record.accumulatedReward]
      self.results[iteration]["NoVisitedStates"] = [record.noVisitedStates]
    else: 
      self.results[iteration]["ConfusionMatrix"].merge(record.confusionMatrix)
      self.results[iteration]["AccumulatedReward"].append(record.accumulatedReward)
      self.results[iteration]["NoVisitedStates"].append(record.noVisitedStates)
    
  def toJSON(self):
    return { iteration: self._iterationToJson(iteration) for iteration in self.results.keys()}
  
  def _iterationToJson(self, iteration):
    return {"ConfusionMatrix": self.results[iteration]["ConfusionMatrix"].toJSON(),
            "AccumulatedReward": self.results[iteration]["AccumulatedReward"],
            "NoVisitedStates": self.results[iteration]["NoVisitedStates"],}


