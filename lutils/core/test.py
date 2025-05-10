# external packages
import pandas as pd
from typing import Union
# internal packages
from . import log
from .data import Simulation
from .test_utils import *


def compare_profiles(sim1: Simulation,
                     sim2: Simulation,
                     profile: str,
                     profile_value: float,
                     out_log: bool = True):
    pass

# compares surface normals to interpolations points, returns unsatisfactory cells
def int_check(sim: Simulation,
              out_log: bool = True) -> pd.DataFrame:
    df = sim.interpolation_info.get_data()
    vec1 = pd.DataFrame()

    # calculate the distance between first and last point
    vec1["x"] = df["xIntPoint3"].subtract(df["xIntPoint1"])
    vec1["y"] = df["yIntPoint3"].subtract(df["yIntPoint1"])
    vec1["z"] = df["zIntPoint3"].subtract(df["zIntPoint1"])

    # calculate normal
    mag = magnitude(vec1)
    # normalize vector
    vec1 = vec1.div(mag, axis=0)

    # get surface normal
    vec2 = df.loc[:, ["xSurfNorm", "ySurfNorm", "zSurfNorm"]]
    # rename columns
    vec2 = vec2.rename(columns={"xSurfNorm": "x", "ySurfNorm": "y", "zSurfNorm": "z"})
    # compare normals
    vec1 = vec1.subtract(vec2, axis=1)

    # replace and drop empty rows
    vec1 = isclose_replace(vec1)
    vec1 = vec1.loc[:, ["x", "y", "z"]].dropna(how="all")
    # concatenate cell ids and restructure
    vec1 = vec1.join(df["cellI"], how="left")
    vec1 = vec1.loc[:, ["cellI", "x", "y", "z"]]

    # log output
    if out_log:
        out_log_int = log.IntLog()
        out_log_int.concat(vec1)
        out_log_int.write("log.int")

    return vec1

def ds():
    pass












# # compares the field profile of simple and hfdibrans simulations
# def compare_profile(simple_dat: str,
#                     hfdibrans_dat: str,
#                     profile: str,
#                     profile_value: float,
#                     out_log: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
#     # read data
#     simple = pd.read_csv(simple_dat)
#     hfdibrans = pd.read_csv(hfdibrans_dat)
#     # get needed values
#     simple = sort_and_trim(simple, profile, profile_value)
#     hfdibrans = sort_and_trim(hfdibrans, profile, profile_value)
#     # sort
#     simple.sort_values(by=profile)
#     hfdibrans.sort_values(by=profile)
#     # output log
#     if out_log:
#         out_log_simple = log.ProfileLog()
#         out_log_simple.concat(simple)
#         out_log_simple.write("log.profile_simple")
#
#         out_log_hfdibrans = log.ProfileLog()
#         out_log_hfdibrans.concat(hfdibrans)
#         out_log_hfdibrans.write("log.profile_hfdibrans")
#
#     return simple, hfdibrans
#
# # checks distance to wall, returns unsatisfactory cells
# def ds(sim_data: Union[data.BFSData, data.NACAData],
#        x_step: float,
#        y_step: float,
#        out_log: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
#     # calculate ds difference for cells in x-dir
#     if isinstance(sim_data, data.BFSData):
#         lambda_x, lambda_y = sim_data.return_data(split=True)
#         lambda_x["ds"] = ((lambda_x["xCellCenter"] - lambda_x["xIntPoint1"])
#                                 -(lambda_x["xCellCenter"] - x_step))
#         # reduce dataframe
#         x = lambda_x.loc[:, ["cellI", "ds"]]
#         # replace and drop empty rows
#         x["ds"] = isclose_replace(x["ds"])
#         x = x.dropna()
#
#         # calculate ds difference for cells in y-dir
#         lambda_y["ds"] = ((lambda_y["yCellCenter"] - lambda_y["yIntPoint1"])
#                                     -(lambda_y["yCellCenter"] - y_step))
#         # reduce dataframe
#         y = lambda_y.loc[:, ["cellI", "ds"]]
#         # replace and drop empty rows
#         y["ds"] = isclose_replace(y["ds"])
#         y = y.dropna()
#
#         # log output
#         if out_log:
#             out_log = log.DsLog()
#             out_log.concat(x)
#             out_log.concat(y)
#             out_log.write("log.ds")
#
#         return x, y
#     elif isinstance(sim_data, data.NACAData):
#         pass
#     else:
#         raise TypeError("Incorrect data object input.")
