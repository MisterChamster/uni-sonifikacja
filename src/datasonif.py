import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
# from src.utils import get_peak_coordinates



class DataSonif():
    file_path:  str
    data_array: np.ndarray
    min_val:    float
    max_val:    float
    treshold:   float
    normalized: bool

    def __init__(self, file_path: str, segment: int):
        self.file_path  = file_path
        self.treshold   = None
        self.normalized = False

        if segment is None:
            try:
                self.data_array = pd.read_csv(
                                    self.file_path,
                                    header=None,
                                    names=["values"],
                                    skipinitialspace=True)
            except:
                raise Exception("Data loading has failed.\n")
        else:
            try:
                self.data_array = pd.read_csv(
                                    self.file_path,
                                    header=None,
                                    names=["values"],
                                    skiprows=lambda i: i % segment != 0,
                                    skipinitialspace=True)
            except:
                raise Exception("Data loading has failed.\n")
        self.data_array = self.data_array.to_numpy()

        self.update_min_max()


    def update_min_max(self) -> None:
        self.min_val = float(np.min(self.data_array))
        self.max_val = float(np.max(self.data_array))
        return None


    # Normalization xnorm = (x-xmin)/(xmax-xmin)
    def normalize_data(self) -> None:
        if self.normalized == True:
            return None

        difference = self.max_val - self.min_val
        self.data_array = (self.data_array - self.min_val)/(difference)

        self.update_min_max()

        # Take care here when treshold function works
        # if self.treshold is not None:
        # self.treshold = 
        self.normalized = True
        return None


    def calculate_treshold(self) -> None:
        pass


    def show_chart(self) -> None:
        # Getting x signs for evey state approximate midpoint
        # peak_coords = get_peak_coordinates(self.file_path, 2000, self.min_val, self.max_val)
        # peak_xes = [a[0] for a in peak_coords]
        # peak_ys  = [a[1] for a in peak_coords]
        # if self.normalized == True:
        #     difference = self.max_val - self.min_val
        #     for i in range(len(peak_ys)):
        #         peak_ys[i] = (peak_ys[i]-self.min_val)/(difference)
        # plt.scatter(peak_xes, peak_ys, marker="x", colorizer="red", s=220, linewidths=3)
        plt.scatter(np.arange(self.data_array.shape[0]), self.data_array, s=1)

        plt.gca().xaxis.set_major_locator(MultipleLocator(240000/10))
        if self.normalized == True:
            y_locators = 0.1
        else:
            y_locators = 1
        plt.gca().yaxis.set_major_locator(MultipleLocator(y_locators))

        plt.xlabel("Sample index")
        if self.normalized == True:
            plt.ylabel("Normalised Voltage")
        else:
            plt.ylabel("Voltage [V]")
        plt.title('Open and closed states of the ion canal in time (perceived in samples)')

        plt.show()

        return None


    def show_histogram(self) -> None:
        plt.hist(self.data_array, bins=200)

        plt.ylabel("Sample index")
        if self.normalized == True:
            plt.xlabel("Normalised Voltage")
        else:
            plt.xlabel("Voltage [V]")
        plt.title('Histogram of number of samples per voltage')

        plt.show()
