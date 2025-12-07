import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator



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
            self.data_array = pd.read_csv(
                                self.file_path,
                                header=None,
                                names=["values"],
                                skipinitialspace=True)
        else:
            self.data_array = pd.read_csv(
                                self.file_path,
                                header=None,
                                names=["values"],
                                skiprows=lambda i: i % segment != 0,
                                skipinitialspace=True)

        self.update_min_max()


    def update_min_max(self) -> None:
        # Get pandas.Series objects and convert them to floats. There was a
        # FutureWarning regarding a blatant type casting to float
        self.min_ds_val = self.data_array.min()
        self.min_ds_val = float(self.min_ds_val["values"])
        self.max_ds_val = self.data_array.max()
        self.max_ds_val = float(self.max_ds_val["values"])
        return None


    # Normalization xnorm = (x-xmin)/(xmax-xmin)
    def normalize_data(self) -> None:
        if self.normalized == True:
            return None

        difference = self.max_ds_val - self.min_ds_val
        loaded_data = loaded_data.map(lambda x: (x-self.min_ds_val)/(difference))

        self.update_min_max()

        # Take care here when treshold function works
        # if self.treshold is not None:
        # self.treshold = 
        self.normalized = True
        return None


    def calculate_treshold(self):
        pass


    def show_chart(self):
        pass


    def show_histogram(self):
        pass
