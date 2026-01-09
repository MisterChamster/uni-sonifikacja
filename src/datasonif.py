import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from pathlib import Path
from typing import Literal
from src.utils import Utils
from src.askers import Askers



class DataSonif():
    file_path:  Path
    data_array: np.ndarray
    data_sign:  str
    og_order:   bool
    og_sign:    bool
    min_val:    float
    max_val:    float
    bins_count: int
    threshold:   float | None
    normalized: bool
    converted_to_binary:     bool
    converted_to_dwelltimes: bool


    def __init__(
        self,
        file_path: Path,
        segment:   int
    ) -> None:
        self.file_path  = file_path
        self.og_order   = True
        self.og_sign    = True

        self.bins_count = 200
        self.threshold   = None
        self.normalized = False
        self.converted_to_binary = False
        self.converted_to_dwelltimes = False

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
        return


    def reverse_data_order(self) -> None:
        self.data_array = self.data_array[::-1]
        self.og_order = not self.og_order
        return


    def reverse_data_sign(self) -> None:
        self.data_array = -self.data_array
        self.show_chart()

        if self.data_sign == "-":
            self.data_sign = "+"
        else:
            self.data_sign = "-"

        self._update_min_max()
        if self.threshold:
            self.calculate_threshold()
        return


    # Normalization xnorm = (x-xmin)/(xmax-xmin)
    def normalize_data(self) -> None:
        if self.normalized == True:
            return

        difference = self.max_val - self.min_val
        self.data_array = (self.data_array - self.min_val)/(difference)

        # Normalize threshold
        if self.threshold:
            # Method calculate_threshold could be used, but calculating 
            # manually saves a ton of computing.
            # self.calculate_threshold()
            self.threshold = (self.threshold - self.min_val)/(difference)

        self._update_min_max()
        self.normalized = True
        return


    # Getting threshold as average between two sample count peaks (open and closed)
    def calculate_threshold(self) -> None:
        # Returns two ndarrays
        sample_count, voltage_val = np.histogram(self.data_array,
                                                 bins=self.bins_count)
        halfarr = int(self.bins_count/2)

        first_peak_index  = np.argmax(sample_count[:halfarr])
        second_peak_index = np.argmax(sample_count[halfarr:]) + halfarr

        threshold_index = (first_peak_index + second_peak_index)/2

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
        # accurate threshold between open/closed states!!

        if threshold_index != int(threshold_index):
            threshold_index = int(threshold_index + 0.5)
            threshold_val = voltage_val[threshold_index]

        elif threshold_index == int(threshold_index):
            threshold_index = int(threshold_index)
            tempval1 = voltage_val[threshold_index]
            tempval2 = voltage_val[threshold_index+1]
            threshold_val = (tempval1+tempval2)/2

        self.threshold = threshold_val
        return


    def apply_paa_aggregation(
        self,
        segment_value:         int,
        segmenting_style:      Literal["count", "size"]
    ) -> None:

        cut_string_paa = Utils.get_val_from_settings_fix(
            "src/settings.json",
            "CUT_REMAINDER_SAMPLES_PAA",
            True)

        if segmenting_style == "count":
            segment_count = segment_value # That many real segments
            segment_size = (len(self.data_array) // (segment_count-1)
                            if not cut_string_paa
                            else len(self.data_array) // (segment_count))

        elif segmenting_style == "size":
            segment_size = segment_value
            #vv That many FIXED-size segments vv
            segment_count = len(self.data_array) // segment_size
            if not cut_string_paa:
                segment_count += 1 # That many real segments

        temparr: np.ndarray = np.empty(segment_count)

        # Cutting data array before segmenting
        if cut_string_paa:
            cut_length: int = len(self.data_array) % segment_count

            if cut_length != 0: #Cut if there's something to cut
                self.data_array = self.data_array[:-cut_length]
        # For additional segment with remaining data (calculated after the loop)
        else:
            segment_count -= 1


        # Putting segment means to temparr
        index_segment: int = 0
        iterative: int     = 0

        while iterative < segment_count:
            segment_sum: np.float64 = 0
            for i in range(index_segment, index_segment+segment_size):
                segment_sum += self.data_array[i]

            segment_mean: np.float64 = segment_sum / segment_size
            temparr[iterative] = segment_mean

            index_segment += segment_size
            iterative += 1

        # Calculating mean of the segment with remaining data (no cutting route)
        if not cut_string_paa:
            segment_sum: np.float64 = 0
            for i in range(index_segment, len(self.data_array)):
                segment_sum += self.data_array[i]
            segment_mean: np.float64 = segment_sum / segment_size
            temparr[iterative] = segment_mean

        self.data_array = temparr
        # Update fields accordingly
        self._update_min_max()
        if self.threshold != None:
            self.calculate_threshold()
        return


    def convert_data_to_binary(self) -> None:
        if not self.normalized:
            self.normalize_data()

        if not self.threshold:
            self.calculate_threshold()

        for i in range(len(self.data_array)):
            self.data_array[i] = (
                0
                if self.data_array[i] <= self.threshold
                else 1)

        self._update_min_max()
        self.converted_to_binary = True
        return


    def __paa_but_binary(
        self,
        segment_value:         int,
        segmenting_style:      Literal["count", "size"]
    ) -> None:

        cut_string_paa = Utils.get_val_from_settings_fix(
            "src/settings.json",
            "CUT_REMAINDER_SAMPLES_DWELLTIMES",
            True)
        if not self.threshold:
            self.calculate_threshold()

        if segmenting_style == "count":
            segment_count = segment_value # That many real segments
            segment_size = (len(self.data_array) // (segment_count-1)
                            if not cut_string_paa
                            else len(self.data_array) // (segment_count))

        elif segmenting_style == "size":
            segment_size = segment_value
            #vv That many FIXED-size segments vv
            segment_count = len(self.data_array) // segment_size
            if not cut_string_paa:
                segment_count += 1 # That many real segments

        temparr: np.ndarray = np.empty(segment_count)

        # Cutting data array before segmenting
        if cut_string_paa:
            cut_length: int = len(self.data_array) % segment_count

            if cut_length != 0: #Cut if there's something to cut
                self.data_array = self.data_array[:-cut_length]
        # For additional segment with remaining data (calculated after the loop)
        else:
            segment_count -= 1


        # Putting segment means to temparr
        index_segment: int = 0
        iterative: int     = 0

        while iterative < segment_count:
            segment_sum: int = 0
            for i in range(index_segment, index_segment+segment_size):
                segment_sum += self.data_array[i]

            segment_mean: float = segment_sum / segment_size
            segment_bin_val = 0 if segment_mean <= self.threshold else 1
            temparr[iterative] = segment_bin_val

            index_segment += segment_size
            iterative += 1

        # Calculating mean of the segment with remaining data (no cutting route)
        if not cut_string_paa:
            segment_sum: int = 0
            for i in range(index_segment, index_segment+segment_size):
                segment_sum += self.data_array[i]

            segment_mean: float = segment_sum / segment_size
            segment_bin_val = 0 if segment_mean <= self.threshold else 1
            temparr[iterative] = segment_bin_val

        self.data_array = temparr
        # Update fields accordingly
        self._update_min_max()
        self.calculate_threshold()
        return


    def convert_to_dwell_times(
        self,
        segment_value:    int,
        segmenting_style: str
    ) -> None:

        if not self.converted_to_binary:
            self.convert_data_to_binary()

        # PAA SHOULD NOT BE USED HERE YOU DUMDUM

        self.__paa_but_binary(
            segment_value,
            segmenting_style)
        self.converted_to_dwelltimes = True
        return


    def sonify_loop(
        self,
        settings_rel_adress: str,
        notes_rel_adress: str
    ) -> None:
        asker_sonif_type = Askers.ask_sonif_type(
            self.converted_to_binary,
            #COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE
            # COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE COME_BACK_HER
            #COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE
            # COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE COME_BACK_HER
            False)
        print("\n\n")

        if not asker_sonif_type:
            return
        if asker_sonif_type == "binary":
            self.binary_sonif_loop(settings_rel_adress, notes_rel_adress)
            return
        elif asker_sonif_type == "analog":
            # CONTINUE WRITING HERE
            # self.analog_sonif_loop(settings_rel_adress, notes_rel_adress)
            return


    def binary_sonif_loop(
        self,
        settings_rel_adress: str,
        notes_rel_adress: str
    ) -> None:
        sample_rate: int = Utils.get_val_from_settings_fix(
            settings_rel_adress,
            "SAMPLE_RATE",
            44100)
        low_note_name: str = Utils.get_val_from_settings_fix(
            settings_rel_adress,
            "BINARY_SONIFICATION_LOW_NOTE",
            "D3")
        high_note_name: str = Utils.get_val_from_settings_fix(
            settings_rel_adress,
            "BINARY_SONIFICATION_HIGH_NOTE",
            "A4")
        note_len_milis: int = Utils.get_val_from_settings_fix(
            settings_rel_adress,
            "BINARY_SONIFICATION_NOTE_LENGTH_MILIS",
            "300")

        while True:
            print("Sonification type: Binary")
            print(f"Low note:    {low_note_name}")
            print(f"High note:   {high_note_name}")
            print(f"Note duration (ms): {note_len_milis}")
            print(f"Sample rate: {sample_rate}")
            print("")
            break

        return


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
        plt.scatter(np.arange(self.data_array.shape[0]),
                              self.data_array,
                              s=1)

        # Threshold line
        if self.threshold:
            plt.axhline(y=self.threshold, color="red")

        # plt.gca().xaxis.set_major_locator(MultipleLocator(len(self.data_array)/10))
        y_locators = 0.1 if self.normalized == True else 1
        plt.gca().yaxis.set_major_locator(MultipleLocator(y_locators))

        plt.xlabel("Sample index")
        if self.normalized:
            plt.ylabel("Normalised Voltage")
        else:
            plt.ylabel("Voltage [V]")
        plt.title('Open and closed states of the ion canal in time (perceived in samples)')

        plt.show()

        return


    def show_histogram(self) -> None:
        plt.hist(self.data_array, bins=self.bins_count)

        # Threshold line
        if self.threshold is not None:
            plt.axvline(x=self.threshold, color="red")

        plt.ylabel("Sample count")
        if self.normalized == True:
            plt.xlabel("Normalised Voltage")
        else:
            plt.xlabel("Voltage [V]")
        plt.title('Histogram of number of samples per voltage')

        plt.show()
        return


    def get_sample_count(self) -> int:
        return len(self.data_array)
