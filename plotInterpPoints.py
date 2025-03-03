import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import checkLambda as cl

nCellsY = 10
loadPath = "interpolationInfo_surface.dat"
savePath = ""

plotData = cl.intInfo(loadPath, nCellsY)
plotData.load()
cellX, cellY = plotData.returnDF()

def xComparisonPlot(dataFrame, savePath, rows=None):

    if rows == None: 
        fig = plt.figure()
        plt.scatter(dataFrame.loc[:, "xCellCenter"], dataFrame.loc[:, "yCellCenter"], color="black", label="cellCenter")
        plt.scatter(dataFrame.loc[:, "xIntPoint1"], dataFrame.loc[:, "yIntPoint1"], color="red", label="intPoint1")
        plt.scatter(dataFrame.loc[:, "xIntPoint2"], dataFrame.loc[:, "yIntPoint2"], color="green", label="intPoint2")
        plt.scatter(dataFrame.loc[:, "xIntPoint3"], dataFrame.loc[:, "yIntPoint3"], color="orange", label="intPoint3")
        plt.vlines(1.0, 0, 0.01, label="xStep")
        fig.legend()
        fig.savefig(savePath)
        return None
    
    fig = plt.figure()
    plt.scatter(dataFrame.loc[rows[0]:rows[1], "xCellCenter"], dataFrame.loc[rows[0]:rows[1], "yCellCenter"], color="black", label="cellCenter")
    plt.scatter(dataFrame.loc[rows[0]:rows[1], "xIntPoint1"], dataFrame.loc[rows[0]:rows[1], "yIntPoint1"], color="red", label="intPoint1")
    plt.scatter(dataFrame.loc[rows[0]:rows[1], "xIntPoint2"], dataFrame.loc[rows[0]:rows[1], "yIntPoint2"], color="green", label="intPoint2")
    plt.scatter(dataFrame.loc[rows[0]:rows[1], "xIntPoint3"], dataFrame.loc[rows[0]:rows[1], "yIntPoint3"], color="orange", label="intPoint3")
    plt.vlines(1.0, dataFrame.loc[rows[0], "yCellCenter"], dataFrame.loc[rows[1], "yCellCenter"], label="xStep")
    fig.legend()
    fig.savefig(savePath)

def yComparisonPlot(dataFrame, savePath, rows=None):

    if rows == None: 
        fig = plt.figure()
        plt.scatter(dataFrame.loc[:, "xCellCenter"], dataFrame.loc[:, "yCellCenter"], color="black", label="cellCenter")
        plt.scatter(dataFrame.loc[:, "xIntPoint1"], dataFrame.loc[:, "yIntPoint1"], color="red", label="intPoint1")
        plt.scatter(dataFrame.loc[:, "xIntPoint2"], dataFrame.loc[:, "yIntPoint2"], color="green", label="intPoint2")
        plt.scatter(dataFrame.loc[:, "xIntPoint3"], dataFrame.loc[:, "yIntPoint3"], color="orange", label="intPoint3")
        plt.hlines(0.01, 0.0, 1.0, label="yStep")
        fig.legend()
        fig.savefig(savePath)
        return None
    
    fig = plt.figure()
    plt.scatter(dataFrame.loc[rows[0]:rows[1], "xCellCenter"], dataFrame.loc[rows[0]:rows[1], "yCellCenter"], color="black", label="cellCenter")
    plt.scatter(dataFrame.loc[rows[0]:rows[1], "xIntPoint1"], dataFrame.loc[rows[0]:rows[1], "yIntPoint1"], color="red", label="intPoint1")
    plt.scatter(dataFrame.loc[rows[0]:rows[1], "xIntPoint2"], dataFrame.loc[rows[0]:rows[1], "yIntPoint2"], color="green", label="intPoint2")
    plt.scatter(dataFrame.loc[rows[0]:rows[1], "xIntPoint3"], dataFrame.loc[rows[0]:rows[1], "yIntPoint3"], color="orange", label="intPoint3")
    plt.hlines(0.01, dataFrame.loc[rows[0], "xCellCenter"], dataFrame.loc[rows[1], "xCellCenter"], label="yStep")
    fig.legend()
    fig.savefig(savePath)

def xLinePlot(dataFrame, savePath, row=0, step=True):

    x = np.array([dataFrame.loc[row, "xCellCenter"], dataFrame.loc[row, "xIntPoint1"], dataFrame.loc[row, "xIntPoint2"], dataFrame.loc[row, "xIntPoint3"]])
    y = np.array([dataFrame.loc[row, "yCellCenter"], dataFrame.loc[row, "yIntPoint1"], dataFrame.loc[row, "yIntPoint2"], dataFrame.loc[row, "yIntPoint3"]])

    A = np.stack([x, np.ones(len(x))]).transpose()
    a, b = np.linalg.lstsq(A, y, rcond=None)[0]

    fig = plt.figure()
    plt.scatter(dataFrame.loc[row, "xCellCenter"], dataFrame.loc[row, "yCellCenter"], color="black", label="cellCenter")
    plt.scatter(dataFrame.loc[row, "xIntPoint1"], dataFrame.loc[row, "yIntPoint1"], color="red", label="intPoint1")
    plt.scatter(dataFrame.loc[row, "xIntPoint2"], dataFrame.loc[row, "yIntPoint2"], color="green", label="intPoint2")
    plt.scatter(dataFrame.loc[row, "xIntPoint3"], dataFrame.loc[row, "yIntPoint3"], color="orange", label="intPoint3")
    plt.plot(x, a*x + b, "k")
    fig.legend()
    fig.savefig(savePath)