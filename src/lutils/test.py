import pandas as pd
import numpy as np
import bisect
import src.lutils.log as log
import src.lutils.data as data
from src.lutils.utility_functions import *

# compares the field profile of simple and hfdibrans
def compare_profile(simple_dat: str, hfdibrans_dat: str, profile: str,
                        profile_value: float, out_log: bool = True):
    # read data
    simple = pd.read_csv(simple_dat)
    hfdibrans = pd.read_csv(hfdibrans_dat)
    # get needed values
    simple = sort_and_trim(simple, profile, profile_value)
    hfdibrans = sort_and_trim(hfdibrans, profile, profile_value)
    # sort
    simple.sort_values(by=profile)
    hfdibrans.sort_values(by=profile)
    # output log
    if out_log:
        out_log_simple = log.ProfileLog()
        out_log_simple.concat(simple)
        out_log_simple.write("log.profile_simple")

        out_log_hfdibrans = log.ProfileLog()
        out_log_hfdibrans.concat(hfdibrans)
        out_log_hfdibrans.write("log.profile_hfdibrans")

    return simple, hfdibrans

def int_check(sim_data: data.SimData, out_log: bool = True):
    vec1 = pd.DataFrame()
    # calculate the distance between first and last point
    vec1["x"] = sim_data.df["xIntPoint3"].subtract(sim_data.df["xIntPoint1"]).copy()
    vec1["y"] = sim_data.df["yIntPoint3"].subtract(sim_data.df["yIntPoint1"]).copy()
    vec1["z"] = sim_data.df["zIntPoint3"].subtract(sim_data.df["zIntPoint1"]).copy()
    
    # calculate normal
    mag = mag(vec1)
    # normalize vector
    vec1 = vec1.div(mag, axis=0)

    # get surface normal
    vec2 = sim_data.df.loc[:, ["xSurfNorm", "ySurfNorm", "zSurfNorm"]].copy()
    # rename columns
    vec2 = vec2.rename(columns={"xSurfNorm": "x", "ySurfNorm": "y", "zSurfNorm": "z"})
    # compare normals
    vec1 = vec1.subtract(vec2, axis=1)
    
    # replace and drop empty rows
    vec1 = isclose_replace(vec1)
    vec1 = vec1.loc[:, ["x", "y", "z"]].dropna(how="all")
    # concatenate cell ids and restructure
    vec1 = vec1.join(sim_data.df["cellI"], how="left")
    vec1 = vec1.loc[:, ["cellI", "x", "y", "z"]]

    # log output
    if out_log_int:
        out_log_int = log.IntLog()
        out_log_int.concat(vec1)
        out_log_int.write("log.int")

def ds(sim_data: data.BFSData | data.NACAData, x_step: float, y_step: float, out: bool = False):
    # calculate ds difference for cells in x-dir
    if isinstance(sim_data, data.BFSData):
        sim_data.lambda_x["ds"] = ((sim_data.lambda_x["xCellCenter"] - sim_data.lambda_x["xIntPoint1"])
                                -(sim_data.lambda_x["xCellCenter"] - x_step))
        # reduce dataframe
        x = sim_data.lambda_x.loc[:, ["cellI", "ds"]]
        # replace and drop empty rows
        x["ds"] = isclose_replace(x["ds"])
        x = x.dropna()

        # calculate ds difference for cells in y-dir
        sim_data.lambda_y["ds"] = ((sim_data.lambda_y["yCellCenter"] - sim_data.lambda_y["yIntPoint1"])
                                    -(sim_data.lambda_y["yCellCenter"] - y_step))
        # reduce dataframe
        y = sim_data.lambda_y.loc[:, ["cellI", "ds"]]
        # replace and drop empty rows
        y["ds"] = isclose_replace(y["ds"])
        y = y.dropna()

        # log output
        if out_log:
            out_log = log.DsLog()
            out_log.concat(x)
            out_log.concat(y)
            out_log.write("log.ds")

        return x, y
    
    elif isinstance(sim_data, data.NACAData):
        pass

    else:
        pass