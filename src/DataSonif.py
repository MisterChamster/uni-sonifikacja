import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
# from src.utils import get_peak_coordinates



class DataSonif():
    file_path:  str
    data_array: pd.core.frame.DataFrame
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

        self.update_min_max()


    def update_min_max(self) -> None:
        # Get pandas.Series objects and convert them to floats. There was a
        # FutureWarning regarding a blatant type casting to float
        self.min_val = self.data_array.min()
        self.min_val = float(self.min_val["values"])
        self.max_val = self.data_array.max()
        self.max_val = float(self.max_val["values"])
        return None


    # Normalization xnorm = (x-xmin)/(xmax-xmin)
    def normalize_data(self) -> None:
        if self.normalized == True:
            return None

        difference = self.max_val - self.min_val
        self.data_array = self.data_array.map(lambda x: (x-self.min_val)/(difference))

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
        plt.scatter(self.data_array.index, self.data_array["values"], s=1)

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
        pass
