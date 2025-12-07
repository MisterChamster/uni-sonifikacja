import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator



class DataSonif():
    file_path:  str
    data_array: pd.core.frame.DataFrame
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

    def normalize_data():
        pass

    def calculate_treshold():
        pass

    def show_chart():
        pass

    def show_histogram():
        pass
