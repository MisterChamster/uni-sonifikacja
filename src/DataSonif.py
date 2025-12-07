import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator



class DataSonif():
    file_path:  str
    data_array: pd.core.frame.DataFrame
    treshold:   float
    normalised: bool

    def __init__(self, file_path: str, segment: int):
        self.file_path  = file_path

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
