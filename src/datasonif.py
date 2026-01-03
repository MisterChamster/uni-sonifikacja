import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from pathlib import Path
import json
# from src.utils import get_peak_coordinates



class DataSonif():
    file_path:  Path
    data_array: np.ndarray
    data_sign:  str
    og_order:   bool
    og_sign:    bool
    min_val:    float
    max_val:    float
    bins_count: int
    treshold:   float | None
    normalized: bool


    def __init__(self, file_path: str, segment: int) -> None:
        self.file_path  = file_path
        self.og_order   = True
        self.og_sign    = True

        self.treshold   = None
        self.normalized = False
        self.bins_count = 200

        if segment == 1:
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

        self.data_array = self.data_array.to_numpy().flatten()
        self.data_sign  = "-" if self.data_array[0] < 0 else "+"

        self._update_min_max()


    def _update_min_max(self) -> None:
        self.min_val = float(np.min(self.data_array))
        self.max_val = float(np.max(self.data_array))
        return None


    def reverse_data_order(self) -> None:
        self.data_array = self.data_array[::-1]
        self.og_order = not self.og_order
        return None


    def reverse_data_sign(self) -> None:
        self.data_array = -self.data_array
        self.og_sign    = not self.og_sign
        return None


    def apply_paa_aggregation(self, segment_count: int) -> None:
        temparr: np.ndarray = np.empty(segment_count)
        with open("src/settings.json") as f:
            config = json.load(f)
            cut_string = config["CUT_REMAINDER_STRING"]

        # Cutting data array before segmenting
        if cut_string == "True":
            cut_length: int = len(self.data_array) % segment_count

            if cut_length != 0: #Cut if there's something to cut
                self.data_array = self.data_array[:-cut_length]
        # For additional segment with cutoff data
        else:
            segment_count -= 1


        segment_size: int   = len(self.data_array) // segment_count
        index_segment: int  = 0
        iterative: int      = 0

        # Putting segment means to temparr
        while iterative < segment_count:
            # print(str(iterative+1) + ".", index_segment, " - ", index_segment+segment_size-1)
            segment_sum: np.float64 = 0
            for i in range(index_segment, index_segment+segment_size):
                segment_sum += self.data_array[i]

            segment_mean: np.float64 = segment_sum / segment_size
            temparr[iterative] = segment_mean

            index_segment += segment_size
            iterative += 1

        # Calculating mean of the segment that wasn't cut off
        if cut_string == "False":
            segment_sum: np.float64 = 0
            for i in range(index_segment, len(self.data_array)):
                segment_sum += self.data_array[i]
            segment_mean: np.float64 = segment_sum / segment_size
            temparr[iterative] = segment_mean

        self.data_array = temparr
        # Update fields
        self._update_min_max()
        if self.treshold != None:
            self.calculate_treshold()

        return None


    # Normalization xnorm = (x-xmin)/(xmax-xmin)
    def normalize_data(self) -> None:
        if self.normalized == True:
            return None

        difference = self.max_val - self.min_val
        self.data_array = (self.data_array - self.min_val)/(difference)

        # Normalize treshold
        if self.treshold is not None:
            # Method calculate_treshold could be used, but calculating 
            # manually saves a ton of computing.
            # self.calculate_treshold()
            self.treshold = (self.treshold - self.min_val)/(difference)

        self._update_min_max()
        self.normalized = True
        return None


    # Getting treshold as average between two sample count peaks (open and closed)
    def calculate_treshold(self) -> None:
        # Returns two ndarrays
        sample_count, voltage_val = np.histogram(self.data_array, bins=self.bins_count)
        halfarr = int(self.bins_count/2)

        first_peak_index  = np.argmax(sample_count[:halfarr])
        second_peak_index = np.argmax(sample_count[halfarr:]) + halfarr

        treshold_index = (first_peak_index + second_peak_index)/2

        # There are more voltages than sample counts. So, if mid index between
        # two peaks is odd, we have to round it up. If midpoint is even, we need
        # to calculate average voltage between index i and i+1.

        # Example 1:
        # Samples:  [1000, 6000, 2000, 3000, 5000, 1000]
        # Voltages: [0, 1.7, 3.3, 5, 6.7, 8.3, 10]

        # Here, our sample peaks are at index 1 and 4. (1+4)/2 = 2.5 => 3
        # 5V has index 3 so it checks

        # Example 2:
        # Samples:  [1000, 6000, 2000, 5000, 1000]
        # Voltages: [0, 2, 4, 6, 8, 10]

        # Here, our sample peaks are at index 1 and 3. (1+3)/2 = 2
        # 4V has index 2, but as we see 2000 samples are between 4 and 6V.
        # Thus, calculating (4+6)/2 = 5V returns us a truest average voltage
        # between two peaks. Keep in mind that average voltage is still not an
        # accurate treshold between open/closed states!!

        if treshold_index != int(treshold_index):
            treshold_index = int(treshold_index + 0.5)
            treshold_val = voltage_val[treshold_index]

        elif treshold_index == int(treshold_index):
            treshold_index = int(treshold_index)
            tempval1 = voltage_val[treshold_index]
            tempval2 = voltage_val[treshold_index+1]
            treshold_val = (tempval1+tempval2)/2

        self.treshold = treshold_val
        return None


    def show_chart(self) -> None:
        # Getting x signs for evey state approximate midpoint
        # peak_coords = get_peak_coordinates(str(self.file_path), 2000, self.min_val, self.max_val)
        # peak_xes = [a[0] for a in peak_coords]
        # peak_ys  = [a[1] for a in peak_coords]
        # if self.normalized == True:
        #     difference = self.max_val - self.min_val
        #     for i in range(len(peak_ys)):
        #         peak_ys[i] = (peak_ys[i]-self.min_val)/(difference)
        # plt.scatter(peak_xes, peak_ys, marker="x", colorizer="red", s=220, linewidths=3)
        plt.scatter(np.arange(self.data_array.shape[0]), self.data_array, s=1)

        # Treshold line
        if self.treshold is not None:
            plt.axhline(y=self.treshold, color="red")

        # plt.gca().xaxis.set_major_locator(MultipleLocator(len(self.data_array)/10))
        y_locators = 0.1 if self.normalized == True else 1
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
        plt.hist(self.data_array, bins=self.bins_count)

        # Treshold line
        if self.treshold is not None:
            plt.axvline(x=self.treshold, color="red")

        plt.ylabel("Sample count")
        if self.normalized == True:
            plt.xlabel("Normalised Voltage")
        else:
            plt.xlabel("Voltage [V]")
        plt.title('Histogram of number of samples per voltage')

        plt.show()


    def get_sample_count(self) -> int:
        return len(self.data_array)
