import json
import numpy as np
import matplotlib.pyplot as plt


def load(filename):
    return json.load(open(filename))


def plotRewards(result):
    it, rm, rs = getIterationsMeanStd(result, "AccumulatedReward")
    plotGraph(it, rm, rs, ["Average accumulated reward", "Standard deviation"],
              "Evolution of obtained reward", "Accumulated Reward", [1, len(it), -1.5, 1.5])


def plotVisitedStates(result):
    it, sm, ss = getIterationsMeanStd(result, "NoVisitedStates")
    plotGraph(it, sm, ss, ["Average visited states", "Standard deviation"],
              "States visited before reaching the goal", "No visited states", [1, len(it), 0, 8])


def getIterationsMeanStd(result, value):
    it = [int(point) for point in result.keys()]
    it.sort()

    r = [result[str(point)][value] for point in it]
    rm = np.mean(r, axis=1)
    rs = np.std(r, axis=1)

    return it, rm, rs


def plotAccuracy(result):
    it = [int(point) for point in result.keys()]
    it.sort()

    accuracy = [result[str(point)]["ConfusionMatrix"]["Accuracy"] for point in it]

    plotGraph(it, accuracy, None, None, "Evolution of accuracy", "Accuracy %", [1, len(it), 0, 105])


def plotPrecisionAndRecall(result, rewardClass):
    it = [int(point) for point in result.keys()]
    it.sort()

    precision = [result[str(point)]["ConfusionMatrix"]["Precision"][str(rewardClass)] for point in it]
    recall = [result[str(point)]["ConfusionMatrix"]["Recall"][str(rewardClass)] for point in it]

    plotGraph(it, precision, recall, ["Precision", "Recall"],
        "Precision and recall for reward {}".format(rewardClass), "%", [1, len(it), 0, 105])


def plotGraph(it, first, second, labels, title, ylabel, axesRange):
    lfirst, = plt.plot(it, first)
    if second != None:
        lsec, = plt.plot(it, second)
        plt.legend([lfirst, lsec], labels, loc = "best")
    plt.xlabel("No of iterations")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.axis(axesRange)
    plt.show()
