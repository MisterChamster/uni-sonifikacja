import pandas as pd
import numpy  as np
import math
import matplotlib.pyplot as plt

from matplotlib.ticker import MultipleLocator
from pathlib           import Path
from typing            import Literal
from scipy.io.wavfile  import write

from src.utils  import Utils
from src.askers import Askers
from src.chunk  import Chunk
from src.note   import Note



class DataSonif():
    file_path:   Path | None
    data_array:  np.ndarray[np.float64] | None
    data_sign:   str | None
    is_og_order: bool | None
    is_og_sign:  bool | None
    min_val:     float | None
    max_val:     float | None
    bins_count:  int
    threshold:   float | None
    is_normalized: bool
    downsampling_performed: list[int]
    is_converted_to_binary: bool

    settings_rel_path: str = "src/settings.json"
    notes_rel_path:    str = "src/notes.json"


    def __init__(self) -> None:
        self.file_path   = None
        self.data_array  = None
        self.data_sign   = None
        self.is_og_order = None
        self.is_og_sign  = None
        self.min_val = None
        self.max_val = None

        self.bins_count = 200
        self.threshold  = None
        self.is_normalized = False
        self.downsampling_performed = []
        self.is_converted_to_binary = False
        return


    def downsample_data(self, n: int) -> None:
        if n > self.get_sample_count():
            print("n is higher than the current number of loaded samples!\n")
            return

        new_sample_count: int = self.get_sample_count() // n
        temparr:   np.ndarray = np.empty(new_sample_count)

        i_new = 0
        for i_dar in range(0, self.get_sample_count(), n):
            temparr[i_new] = self.data_array[i_dar]
            i_new += 1

        self.data_array = temparr
        self.downsampling_performed.append(int)
        return


    def get_datafile_path(self) -> bool:
        print("Choose data file in txt/csv format:")
        datafile_path = Askers.ask_path_filedialog("f", "Choose data txt file")
        if not datafile_path:
            print("No file has been chosen.")
            return False
        if not datafile_path.endswith((".txt", ".csv")):
            print("Wrong file format.")
            return False
        print(f"{datafile_path}\n\n")

        datafile_path = Path(datafile_path)
        self.file_path = datafile_path
        return True


    def load_data(self) -> None:
        asker_downsample: int = Askers.ask_downsampling(True)
        if not asker_downsample:
            return
        print("\n")

        if asker_downsample == 1:
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
                    skiprows=lambda i: i % asker_downsample != 0,
                    skipinitialspace=True)
            except:
                raise Exception("Data loading has failed.\n")

        self.data_array = self.data_array.to_numpy().flatten()
        self.data_sign  = "-" if self.data_array[0] < 0 else "+"

        is_threshold_automatic = Utils.get_val_from_json_fix(
            self.settings_rel_path,
            "AUTOMATIC_THRESHOLD_AT_LOAD")
        if is_threshold_automatic:
            self.calculate_threshold()

        self._update_min_max()
        self.is_og_order = True
        self.is_og_sign  = True
        return


    def _update_min_max(self) -> None:
        self.min_val = float(np.min(self.data_array))
        self.max_val = float(np.max(self.data_array))
        return


    def reverse_data_order(self) -> None:
        self.data_array = self.data_array[::-1]
        self.is_og_order = not self.is_og_order
        return


    def reverse_data_sign(self) -> None:
        self.data_array = -self.data_array

        if self.data_sign == "-":
            self.data_sign = "+"
        else:
            self.data_sign = "-"

        self._update_min_max()
        if self.threshold:
            self.calculate_threshold()
            self.is_og_sign = not self.is_og_sign
        return


    # Normalization xnorm = (x-xmin)/(xmax-xmin)
    def normalize_data(self) -> None:
        if self.is_normalized == True:
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
        self.is_normalized = True
        return


    # Getting threshold as average between two sample count peaks (open and closed)
    def calculate_threshold(self) -> None:
        # Returns two ndarrays
        sample_count, voltage_val = np.histogram(
            self.data_array,
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
            threshold_val   = voltage_val[threshold_index]

        elif threshold_index == int(threshold_index):
            threshold_index = int(threshold_index)
            tempval1 = voltage_val[threshold_index]
            tempval2 = voltage_val[threshold_index+1]
            threshold_val = (tempval1+tempval2)/2

        self.threshold = threshold_val
        return


# ============================== PAA AGGREGATION ==============================
    def apply_paa_aggregation(
        self,
        segment_value:    int,
        segmenting_style: Literal["count", "size"]
    ) -> None:

        cut_string_paa = Utils.get_val_from_json_fix(
            "src/settings.json",
            "CUT_REMAINDER_SAMPLES_PAA")

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

        # Cutting data array before segmenting
        if cut_string_paa:
            cut_length: int = len(self.data_array) % segment_count

            if cut_length != 0: #Cut if there's something to cut
                self.data_array = self.data_array[:-cut_length]
        # For additional segment with remaining data (calculated after the loop)
        else:
            segment_count -= 1


        # Putting segment means to temparr
        index_segment: int  = 0
        iterative:     int  = 0
        temparr: np.ndarray = np.empty(segment_count)

        while iterative < segment_count:
            chunk_end: int     = index_segment + segment_size
            temp_chunk         = Chunk(index_segment, chunk_end, self.data_array[index_segment: chunk_end])
            temparr[iterative] = temp_chunk.get_data_mean()

            index_segment += segment_size
            iterative += 1

        # Calculating mean of the segment with remaining data (no cutting route)
        if not cut_string_paa:
            chunk_end: int     = index_segment + segment_size
            temp_chunk         = Chunk(index_segment, chunk_end, self.data_array[index_segment: chunk_end])
            temparr[iterative] = temp_chunk.get_data_mean()

        self.data_array = temparr
        # Update fields accordingly
        self.is_converted_to_binary = False #if paa perfectly converts to binary, this line will save false data
        self._update_min_max()
        if self.threshold:
            self.calculate_threshold()
        return


# ============================ BINARY CONVERSION ==============================
    def convert_data_to_binary(self) -> None:
        if not self.is_normalized:
            self.normalize_data()

        if not self.threshold:
            self.calculate_threshold()

        for i in range(len(self.data_array)):
            self.data_array[i] = (
                0
                if self.data_array[i] <= self.threshold
                else 1)

        self._update_min_max()
        self.is_normalized = True
        self.is_converted_to_binary = True
        return


# ================================ DWELL TIMES ================================
    def __binary_to_dwelltimes(
        self,
        segment_value:    int,
        segmenting_style: Literal["count", "size"]
    ) -> None:

        cut_string_paa = Utils.get_val_from_json_fix(
            "src/settings.json",
            "CUT_REMAINDER_SAMPLES_DWELLTIMES")
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
            chunk_end: int = index_segment + segment_size
            temp_chunk     = Chunk(index_segment, chunk_end, self.data_array[index_segment: chunk_end])
            segment_mean   = temp_chunk.get_data_mean()

            segment_val = 0 if segment_mean <= self.threshold else 1
            for i in range(index_segment, index_segment+segment_size):
                self.data_array[i] = segment_val

            index_segment += segment_size
            iterative += 1

        # Calculating mean of the segment with remaining data (no cutting route)
        if not cut_string_paa:
            chunk_end: int = index_segment + segment_size
            temp_chunk     = Chunk(index_segment, chunk_end, self.data_array[index_segment: chunk_end])
            segment_mean   = temp_chunk.get_data_mean()

            segment_val = 0 if segment_mean <= self.threshold else 1
            for i in range(index_segment, index_segment+segment_size):
                self.data_array[i] = segment_val

        # Update fields accordingly
        self._update_min_max()
        self.calculate_threshold()
        return


    def convert_to_dwell_times(
        self,
        segment_value:    int,
        segmenting_style: str
    ) -> None:

        if not self.is_converted_to_binary:
            self.convert_data_to_binary()

        self.__binary_to_dwelltimes(
            segment_value,
            segmenting_style)
        return

# =========================== CONDENSED DWELL TIMES ===========================
    def __binary_to_dwelltimes_CONDENSED(
        self,
        segment_value:    int,
        segmenting_style: Literal["count", "size"]
    ) -> None:

        cut_string_paa = Utils.get_val_from_json_fix(
            "src/settings.json",
            "CUT_REMAINDER_SAMPLES_DWELLTIMES")
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

        # Cutting data array before segmenting
        if cut_string_paa:
            cut_length: int = len(self.data_array) % segment_count

            if cut_length != 0: #Cut if there's something to cut
                self.data_array = self.data_array[:-cut_length]
        # For additional segment with remaining data (calculated after the loop)
        else:
            segment_count -= 1


        # Putting segment means to temparr
        index_segment: int  = 0
        iterative: int      = 0
        temparr: np.ndarray = np.empty(segment_count)

        while iterative < segment_count:
            chunk_end: int     = index_segment + segment_size
            temp_chunk: Chunk  = Chunk(index_segment, chunk_end, self.data_array[index_segment: chunk_end])
            chunk_binary_val   = 1 if temp_chunk.get_data_mean()>self.threshold else 0
            temparr[iterative] = chunk_binary_val

            index_segment += segment_size
            iterative += 1

        # Calculating mean of the segment with remaining data (no cutting route)
        if not cut_string_paa:
            chunk_end: int     = index_segment + segment_size
            temp_chunk         = Chunk(index_segment, chunk_end, self.data_array[index_segment: chunk_end])
            temparr[iterative] = temp_chunk.get_data_mean()

        self.data_array = temparr
        # Update fields accordingly
        self._update_min_max()
        self.calculate_threshold()
        return


    def convert_to_dwell_times_CONDENSED(
        self,
        segment_value:    int,
        segmenting_style: str
    ) -> None:

        if not self.is_converted_to_binary:
            self.convert_data_to_binary()

        self.__binary_to_dwelltimes_CONDENSED(
            segment_value,
            segmenting_style)
        return


# ============================ BINARY SONIFICATION ============================
    def binary_sonification_nontest(
        self,
        sample_rate:         int,
        note_duration_milis: int,
        low_note_freq:       float,
        high_note_freq:      float
    ) -> None:
        note_duration_sec = note_duration_milis / 1000
        audio: list = []
        t = np.linspace(0,
                        note_duration_sec,
                        int(sample_rate * note_duration_sec),
                        endpoint=False)

        for val in self.data_array:
            curr_freq = (high_note_freq
                         if val == 1
                         else low_note_freq)
            tone = np.sin(2 * np.pi * curr_freq * t)
            audio.append(tone)

        audio = np.concatenate(audio).astype(np.float32)
        curr_time_str = Utils.get_curr_time_to_name()
        write(f"output/sonif_binary_{curr_time_str}.wav", sample_rate, audio)
        return


    def binary_sonification(
        self,
        sample_rate:         int,
        note_duration_milis: int,
        low_note_freq:       float,
        high_note_freq:      float
    ) -> None:
        note_duration_sec: float = note_duration_milis / 1000
        audio: list = []

        notes_dict = Utils.get_dict_from_json(self.notes_rel_path)
        lowest_note = next(iter(notes_dict))
        lowest_freq = notes_dict[lowest_note]
        longest_wavelen_in_samples: int = math.ceil(sample_rate / lowest_freq)

        first_freq = (high_note_freq
                      if self.data_array[0] == 1
                      else low_note_freq)
        first_note = Note(
            sample_rate,
            first_freq,
            note_duration_milis,
            longest_wavelen_in_samples
        )

        print("BREAK\n"*30)


        for val in self.data_array:
            curr_freq = (high_note_freq
                         if val == 1
                         else low_note_freq)

            tone = np.sin(2 * np.pi * curr_freq * t)
            audio.append(tone)

        audio = np.concatenate(audio).astype(np.float32)
        curr_time_str = Utils.get_curr_time_to_name()
        write(f"output/sonif_binary_{curr_time_str}.wav", sample_rate, audio)
        return





    def binary_sonif_loop(self) -> None:
        low_note_name: str = Utils.get_val_from_json_fix(
            self.settings_rel_path,
            "BINARY_SONIFICATION_LOW_NOTE")
        low_note_freq: float = Utils.get_val_from_json(
            self.notes_rel_path,
            low_note_name)
        high_note_name: str = Utils.get_val_from_json_fix(
            self.settings_rel_path,
            "BINARY_SONIFICATION_HIGH_NOTE")
        high_note_freq: float = Utils.get_val_from_json(
            self.notes_rel_path,
            high_note_name)
        sample_rate: int = Utils.get_val_from_json_fix(
            self.settings_rel_path,
            "SAMPLE_RATE")

        while True:
            note_duration_milis: int = Utils.get_val_from_json_fix(
                self.settings_rel_path,
                "BINARY_SONIFICATION_NOTE_DURATION_MILIS")

            final_length_milis: int = (note_duration_milis *
                                       self.get_sample_count())
            audio_len_human = Utils.human_read_milis(final_length_milis)
            print( "Sonification type:  Binary")
            print(f"Low note:             {low_note_name} ({low_note_freq} Hz)")
            print(f"High note:            {high_note_name} ({high_note_freq} Hz)")
            print(f"Note duration (ms):   {note_duration_milis}")
            print(f"Sample rate:          {sample_rate}")
            print(f"Amount of notes:      {self.get_sample_count()}")
            print(f"Final audio duration: {audio_len_human}")
            # print(f"Final audio length (MILI): {final_length_milis}")
            print()
            print("Choose an action:")
            print("d - Change note duration (ms)")
            print("s - Sonify")
            print("r - Return to main menu\n>> ", end="")
            asker = input().strip().lower()
            print("\n")

            if asker == "r":
                return

            elif asker == "d":
                new_note_duration = Askers.ask_note_duration()
                print("\n\n")
                if not new_note_duration:
                    continue
                Utils.save_value_to_settings(
                    "BINARY_SONIFICATION_NOTE_DURATION_MILIS",
                    new_note_duration)

            elif asker == "s":
                print("Sonifying...")
                try:
                    self.binary_sonification(
                        sample_rate,
                        note_duration_milis,
                        low_note_freq,
                        high_note_freq)
                    print("Done!\n\n")
                except Exception as e:
                    print("An exception occurred during binary sonification")
                    print(e)
                continue

            else:
                print("Invalid input.\n\n")


# ============================ ANALOG SONIFICATION ============================
    def analog_sonification(
        self,
        sample_rate:         int,
        note_duration_milis: int,
        notes_used:          list[str],
        notes_dict:          dict[str, float]
    ) -> None:
        optimal_dict: dict[str, float] = {}
        for notename in notes_used:
            optimal_dict[notename] = notes_dict[notename]

        bin_count: int    = len(notes_used)
        note_duration_sec = note_duration_milis / 1000
        audio: list       = []
        t = np.linspace(0,
                        note_duration_sec,
                        int(sample_rate * note_duration_sec),
                        endpoint=False)

        for value in self.data_array:
            val_bin  = int(value*bin_count)
            val_bin -= (val_bin == 5)
            temp_note_name = notes_used[val_bin]
            temp_note_freq = optimal_dict[temp_note_name]

            tone = np.sin(2 * np.pi * temp_note_freq * t)
            audio.append(tone)

        audio = np.concatenate(audio).astype(np.float32)
        curr_time_str = Utils.get_curr_time_to_name()
        write(f"output/sonif_analog_{curr_time_str}.wav",
              sample_rate,
              audio)
        return


    def analog_sonif_loop(self) -> None:
        impossible_anal_message = (
            "Analog sonification cannot be performed.\n"
            "The issue results from messed settings.json or notes.json.\n"
            "Program does not allow messing these up, so it's likely due to writing directly in these files.\n"
            "To fix it, download both settings.json and notes.json files from repo and replace them in src directory of the project\n"
            "And do not edit these files yourself in the future!")
        sample_rate: int = Utils.get_val_from_json_fix(
            self.settings_rel_path,
            "SAMPLE_RATE")

        notes = Utils.get_keys_from_json(self.notes_rel_path)
        while True:
            lowest_note_name: str = Utils.get_val_from_json_fix(
                self.settings_rel_path,
                "ANAL_SONIFICATION_LOWEST_NOTE")
            lowest_note_freq: float = Utils.get_val_from_json(
                self.notes_rel_path,
                lowest_note_name)
            note_duration_milis: int = Utils.get_val_from_json_fix(
                self.settings_rel_path,
                "ANAL_SONIFICATION_NOTE_DURATION_MILIS")
            notes_used_amount: int = Utils.get_val_from_json_fix(
                self.settings_rel_path,
                "ANAL_SONIFICATION_AMOUNT_OF_USED_NOTES")

            highest_note_name = Utils.get_highest_note_anal_safe(
                notes,
                lowest_note_name,
                notes_used_amount)
            if not highest_note_name:
                print(impossible_anal_message)
                break
            highest_note_freq: float = Utils.get_val_from_json(
                self.notes_rel_path,
                highest_note_name)

            final_length_milis: int = (note_duration_milis *
                                       self.get_sample_count())
            audio_len_human = Utils.human_read_milis(final_length_milis)
            print( "Sonification type:    Analog")
            print(f"Amount of used notes: {notes_used_amount}")
            print(f"Lowest note:          {lowest_note_name} ({lowest_note_freq} Hz)")
            print(f"Highest note:         {highest_note_name} ({highest_note_freq} Hz)")
            print(f"Note duration (ms):   {note_duration_milis}")
            print(f"Sample rate:          {sample_rate}")
            print(f"Amount of notes:      {self.get_sample_count()}")
            print(f"Final audio duration: {audio_len_human}")
            print()
            print("Choose an action:")
            print("d - Change note duration (ms)")
            print("l - Change the lowest note name")
            print("a - Change amount of notes for sonification")
            print("s - Sonify")
            print("r - Return to main menu\n>> ", end="")
            asker = input().strip().lower()
            print("\n\n")


            if asker == "r":
                return

            elif asker == "d":
                new_note_duration = Askers.ask_note_duration()
                print("\n\n")
                if not new_note_duration:
                    continue
                Utils.save_value_to_settings(
                    "ANAL_SONIFICATION_NOTE_DURATION_MILIS",
                    new_note_duration)

            elif asker == "l":
                highest_lowest_note: str = Utils.get_highest_lowest_note_possible_for_amount(
                    notes,
                    notes_used_amount)
                new_lowest_note = Askers.ask_lowest_note_anal(
                    lowest_note_name,
                    highest_lowest_note,
                    notes)
                print("\n\n")
                if not new_lowest_note:
                    continue

                Utils.save_value_to_settings(
                    "ANAL_SONIFICATION_LOWEST_NOTE",
                    new_lowest_note)

            elif asker == "a":
                amount_asker = Askers.ask_note_amount(len(notes))
                if not amount_asker or amount_asker == notes_used_amount:
                    continue

                # If lower than previous - save to settings. Highest note will
                # recalculate itself in next loop iteration.
                if amount_asker < notes_used_amount:
                    Utils.save_value_to_settings(
                        "ANAL_SONIFICATION_AMOUNT_OF_USED_NOTES",
                        amount_asker)
                    continue

                # If higher then previous - check if exceeds available notes
                    # If no  - increase note amount
                    # If yes - calculate highest lowest note for amount. Save it and new amount
                elif amount_asker > notes_used_amount:
                    is_possible = Utils._is_anal_possible(
                        notes,
                        lowest_note_name,
                        amount_asker)
                    if is_possible:
                        Utils.save_value_to_settings(
                            "ANAL_SONIFICATION_AMOUNT_OF_USED_NOTES",
                            amount_asker)
                        continue

                    new_lowest_note: str = Utils.get_highest_lowest_note_possible_for_amount(
                        notes,
                        amount_asker)
                    Utils.save_value_to_settings(
                        "ANAL_SONIFICATION_LOWEST_NOTE",
                        new_lowest_note)
                    Utils.save_value_to_settings(
                        "ANAL_SONIFICATION_AMOUNT_OF_USED_NOTES",
                        amount_asker)
                    print("[WARNING] A higher amount of notes forces the lowest note to be lowered")
                    print(f"Previous lowest note: {lowest_note_name}")
                    print(f"Updated lowest note:  {new_lowest_note}")

            elif asker == "s":
                print("Sonifying...")
                notes_dict = Utils.get_dict_from_json(self.notes_rel_path)
                notes_used = Utils.get_notes_used_list(
                    notes,
                    lowest_note_name,
                    notes_used_amount)
                try:
                    self.analog_sonification(
                        sample_rate,
                        note_duration_milis,
                        notes_used,
                        notes_dict)
                    print("Done!\n\n")
                except Exception as e:
                    print("An exception occurred during analog sonification")
                    print(e)
                continue

            else:
                print("Invalid input.\n\n")


# ================================= PLOTTING ==================================
    def show_chart(self) -> None:
        # Getting x signs for evey state approximate midpoint
        # peak_coords = get_peak_coordinates(str(self.file_path), 2000, self.min_val, self.max_val)
        # peak_xes = [a[0] for a in peak_coords]
        # peak_ys  = [a[1] for a in peak_coords]
        # if self.is_normalized == True:
        #     difference = self.max_val - self.min_val
        #     for i in range(len(peak_ys)):
        #         peak_ys[i] = (peak_ys[i]-self.min_val)/(difference)
        # plt.scatter(peak_xes, peak_ys, marker="x", colorizer="red", s=220, linewidths=3)
        plt.scatter(np.arange(self.data_array.shape[0]),
                              self.data_array,
                              s=1)

        # Threshold line
        show_thold: bool = Utils.get_val_from_json_fix(
            self.settings_rel_path,
            "SHOW_THRESHOLD_ON_CHARTS")
        if show_thold and self.threshold:
            plt.axhline(y=self.threshold, color="red")

        # plt.gca().xaxis.set_major_locator(MultipleLocator(len(self.data_array)/10))
        y_locators = 0.1 if self.is_normalized == True else 1
        plt.gca().yaxis.set_major_locator(MultipleLocator(y_locators))

        plt.xlabel("Sample index")
        if self.is_normalized:
            plt.ylabel("Normalised Voltage")
        else:
            plt.ylabel("Voltage [V]")
        plt.title('Open and closed states of the ion channel in time (perceived in samples)')

        plt.show()
        return


    def show_histogram(self) -> None:
        plt.hist(self.data_array, bins=self.bins_count)

        # Threshold line
        show_thold: bool = Utils.get_val_from_json_fix(
            self.settings_rel_path,
            "SHOW_THRESHOLD_ON_CHARTS")
        if show_thold and self.threshold:
            plt.axvline(x=self.threshold, color="red")

        plt.ylabel("Sample count")
        if self.is_normalized == True:
            plt.xlabel("Normalised Voltage")
        else:
            plt.xlabel("Voltage [V]")
        plt.title('Histogram of number of samples per voltage')

        plt.show()
        return


# ================================== GETTERS ==================================
    def get_sample_count(self) -> int:
        return len(self.data_array)
