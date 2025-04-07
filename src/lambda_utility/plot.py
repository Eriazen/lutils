import pandas as pd
import src.lambda_utility.test as test
import numpy as np
import matplotlib.pyplot as plt


class SimPlot:
    def __init__(self, testObj: test.SimTest):
        self._test = testObj
        self._df = testObj._df

    def plot_int_points(self):
        pass

    def plot_ds(self):
        pass
    
    def plot_profile(self, simple_dat: str, hfdibrans_dat: str, profile: str, profile_value: float, field: str):
        # get dataframes
        simple, hfdibrans = self._test.compare_profile(simple_dat, hfdibrans_dat,
                                                       profile, profile_value, out=True)
        # # get plot variables
        # simple = simple[[profile, field]]
        # hfdibrans = hfdibrans[[profile, field]]

        # plot figure
        fig = plt.figure(0, figsize=(20, 12))
        plt.plot(simple[profile], simple[field])
        plt.plot(hfdibrans[profile], hfdibrans[field])

        fig.savefig("test.png")

