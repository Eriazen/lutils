from __future__ import annotations
import pandas as pd
import datetime

class intInfo:
    def __init__(self, loadPath, nCellsY) -> intInfo:
        self.loadPath = loadPath
        self.nCellsY = nCellsY

    def load(self) -> None:
        intInfo = pd.read_csv(self.loadPath)
        intInfo["cellCenter"] = intInfo["cellCenter"].str.split()
        intInfo["intPoints"] = intInfo["intPoints"].str.strip("123456789")
        intInfo["intPoints"] = intInfo["intPoints"].str.split()

        cellX = pd.DataFrame({"cellI": intInfo.loc[0:self.nCellsY-2, "cellI"]})
        cellX["xCellCenter"], cellX["yCellCenter"], cellX["zCellCenter"] = zip(*list(intInfo.loc[0:self.nCellsY-2 ,"cellCenter"].values))
        cellX["xIntPoint1"], cellX["yIntPoint1"], cellX["zIntPoint1"], cellX["xIntPoint2"], cellX["yIntPoint2"], cellX["zIntPoint2"], cellX["xIntPoint3"], cellX["yIntPoint3"], cellX["zIntPoint3"] = zip(*list(intInfo.loc[0:self.nCellsY-2 ,"intPoints"].values))
        cellX = cellX.astype("string").applymap(lambda x: x.strip("()"))
        self.cellX = cellX.apply(pd.to_numeric).reset_index(drop=True)

        cellY = pd.DataFrame({"cellI": intInfo.loc[self.nCellsY-1:, "cellI"]})
        cellY["xCellCenter"], cellY["yCellCenter"], cellY["zCellCenter"] = zip(*list(intInfo.loc[self.nCellsY-1: ,"cellCenter"].values))
        cellY["xIntPoint1"], cellY["yIntPoint1"], cellY["zIntPoint1"], cellY["xIntPoint2"], cellY["yIntPoint2"], cellY["zIntPoint2"], cellY["xIntPoint3"], cellY["yIntPoint3"], cellY["zIntPoint3"] = zip(*list(intInfo.loc[self.nCellsY-1: ,"intPoints"].values))
        cellY = cellY.astype("string").applymap(lambda x: x.strip("()"))
        self.cellY = cellY.apply(pd.to_numeric).reset_index(drop=True)
    
    def dsCompute(self, xStep, yStep) -> None:
        self.cellX["dsDiff"] = ((self.cellX["xCellCenter"] - self.cellX["xIntPoint1"]) - (self.cellX["xCellCenter"] - xStep)).abs()
        self.cellY["dsDiff"] = ((self.cellY["yCellCenter"] - self.cellY["yIntPoint1"]) - (self.cellY["yCellCenter"] - yStep)).abs()

    def diffCompute(self, row=0) -> None:
        self.cellX["xDiffC"] = self.cellX["xCellCenter"] - self.cellX.loc[row, "xCellCenter"]
        self.cellX["xDiff1"] = self.cellX["xIntPoint1"] - self.cellX.loc[row, "xIntPoint1"]
        self.cellX["xDiff2"] = self.cellX["xIntPoint2"] - self.cellX.loc[row, "xIntPoint2"]

        self.cellY["yDiffC"] = self.cellY["yCellCenter"] - self.cellY.loc[row, "yCellCenter"]
        self.cellY["yDiff1"] = self.cellY["yIntPoint1"] - self.cellY.loc[row, "yIntPoint1"]
        self.cellY["yDiff2"] = self.cellY["yIntPoint2"] - self.cellY.loc[row, "yIntPoint2"]

    def returnDF(self) -> pd.DataFrame:
        return self.cellX, self.cellY

    def writeLog(self, savePath, error=1e-11):
        log = open(savePath + "log.checkLambda", "w")
        log.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n\n"))

        log.write("--------------------------------------Vertical cells--------------------------------------\n")
        fcount = 0
        for i in range(self.cellX.shape[0]):
            if self.cellX.loc[i, "xDiffC"] > error:
                log.write("     -> cellCenterOutOfLine: difference %.10f corresponding to cell no. %i.\n" % (self.cellX.loc[i, "xDiffC"], self.cellX.loc[i, "cellI"]))
                fcount += 1
        if fcount == 0: log.write("     -> Cell centers are OK.\n")

        log.write("---------------------------------------------------------------------------\n")
        fcount = 0
        for i in range(self.cellX.shape[0]):
            if self.cellX.loc[i, "xDiff1"] > error:
                log.write("     -> firstIntPointOutOfLine: difference of %.10f corresponding to cell no. %i.\n" % (self.cellX.loc[i, "xDiff1"], self.cellX.loc[i, "cellI"]))
                fcount += 1
        if fcount == 0: log.write("     -> First interpolation points are OK.\n")

        log.write("---------------------------------------------------------------------------\n")

        fcount = 0
        for i in range(self.cellX.shape[0]):
            if self.cellX.loc[i, "xDiff2"] > error:
                log.write("     -> secondIntPointOutOfLine: difference of %.10f corresponding to cell no. %i.\n" % (self.cellX.loc[i, "xDiff2"], self.cellX.loc[i, "cellI"]))
                fcount += 1
        if fcount == 0: log.write("     -> Second interpolation points are OK.\n")

        log.write("---------------------------------------------------------------------------\n")
        fcount = 0
        for i in range(self.cellX.shape[0]):
            if self.cellX.loc[i, "dsDiff"] > error:
                log.write("     -> dsNotEqual: difference of %.10f corresponding to cell no. %i.\n" % (self.cellX.loc[i, "dsDiff"], self.cellX.loc[i, "cellI"]))
                fcount += 1
        if fcount == 0: log.write("     -> Every ds is equal.\n")

        # check lambda and print incosistent cells of cellY
        log.write("\n\n--------------------------------------Horizontal cells--------------------------------------\n")
        fcount = 0
        for i in range(self.cellY.shape[0]):
            if self.cellY.loc[i, "yDiffC"] > error:
                log.write("     -> cellCenterOutOfLine: difference %.10f corresponding to cell no. %i.\n" % (self.cellY.loc[i, "yDiffC"], self.cellY.loc[i, "cellI"]))
                fcount += 1
        if fcount == 0: log.write("     -> Cell centers are OK.\n")

        log.write("---------------------------------------------------------------------------\n")
        fcount = 0
        for i in range(self.cellY.shape[0]):
            if self.cellY.loc[i, "yDiff1"] > error:
                log.write("     -> firstIntPointOutOfLine: difference %.10f corresponding to cell no. %i.\n" % (self.cellY.loc[i, "yDiff1"], self.cellY.loc[i, "cellI"]))
                fcount += 1
        if fcount == 0: log.write("     -> First interpolation points are OK.\n")

        log.write("---------------------------------------------------------------------------\n")
        fcount = 0
        for i in range(self.cellY.shape[0]):
            if self.cellY.loc[i, "yDiff2"] > error:
                log.write("     -> secondIntPointOutOfLine: difference %.10f corresponding to cell no. %i.\n" % (self.cellY.loc[i, "yDiff2"], self.cellY.loc[i, "cellI"]))
                fcount += 1
        if fcount == 0: log.write("     -> Second interpolation points are OK.\n")

        log.write("---------------------------------------------------------------------------\n")
        fcount = 0
        for i in range(self.cellY.shape[0]):
            if self.cellY.loc[i, "dsDiff"] > error:
                log.write("     -> dsNotEqual: difference of %.10f corresponding to cell no. %i.\n" % (self.cellY.loc[i, "dsDiff"], self.cellY.loc[i, "cellI"]))
                fcount += 1
        if fcount == 0: log.write("     -> Every ds is equal.\n")

        log.close()