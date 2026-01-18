import os
from tkinter import filedialog
from typing  import Literal

from src.utils import Utils



class Askers():
    settings_rel_path: str = "src/settings.json"
    notes_rel_path:    str = "src/notes.json"


    @staticmethod
    def ask_path_filedialog(
        node_type: str,
        message:   str
    ) -> str:
        original_path = os.getcwd()
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        os.chdir(desktop_path)

        sel_path = ""
        if node_type == "f":
            sel_path = filedialog.askopenfilename(title=message)
        elif node_type == "d":
            sel_path = filedialog.askdirectory(title=message)

        os.chdir(original_path)
        return sel_path


    @staticmethod
    def ask_downsampling(is_initial: bool = False) -> int|None:
        stroing = ("Input 'exit' to exit program."
                   if is_initial
                   else "Input 'r' to return.")

        while True:
            print("Downsample data (Pick every n-th line of data)\n"
                  "Max value is 10, but highest reasonable is 5.\n"
                 f"Press Enter to skip. {stroing}\n"
                  "n = ", end="")
            asker = input().strip().lower()

            if not asker:
                return 1
            if (asker == "exit" and is_initial) or (asker == "r" and not is_initial):
                return
            if not asker.isdigit():
                print("Incorrect input.\n\n")
                continue

            asker = int(asker)
            if asker < 1:
                return 1
            elif asker > 10:
                print("Input too high.\n\n")
            else:
                return asker


    @staticmethod
    def ask_action() -> str:
        returns_dict = {
            "p": "process_data",
            "s": "sonify",
            "c": "show_chart",
            "h": "show_histogram",
            "t": "settings",
            "f": "change_file",
            "exit": "exit"}

        while True:
            print("Choose an action:\n"
                  "p - Process data...\n"
                  "s - Sonify data...\n"
                  "c - Show chart\n"
                  "h - Show histogram\n"
                  "t - Settings...\n"
                  "f - Change file\n"
                  "exit - Exit program\n>> ", end="")
            asker = input().strip().lower()

            if asker not in returns_dict:
                print("Invalid input!\n")
            else:
                return returns_dict[asker]


    @staticmethod
    def ask_process_data(
        is_normalized: str,
        is_threshold:  str,
        is_binary:     str
    ) -> str | None:
        returns_dict = {
            "x": "reverse_order",
            "y": "reverse_sign",
            "n": "normalization",
            "t": "calculate_threshold",
            "d": "downsample_data",
            "p": "apply_paa",
            "b": "convert_to_bin",
            "t": "convert_to_dwelltimes",
            "c": "convert_to_dwelltimes_condensed",
            "e": "appy_emd",
            "o": "original_data",
            "r": None}
        normalized_msg = "already normalized" if is_normalized else "not normalized"
        threshold_msg  = "already calculated" if is_threshold  else "not calculated"
        binary_msg     = "already converted"  if is_binary     else "not converted"

        while True:
            print("Choose an action:\n"
                  "x - Reverse data order\n"
                  "y - Reverse data sign\n"
                 f"n - Normalize data ({normalized_msg})\n"
                 f"t - Calculate threshold ({threshold_msg})\n"
                  "d - Downsample data\n"
                  "p - Apply PAA downsampling\n"
                 f"b - Convert data to binary ({binary_msg})\n"
                  "t - Convert data to dwell times\n"
                  "c - Convert data to condensed dwell times\n"
                  "e - Apply EMD method\n"
                  "o - Revert to original data set\n"
                  "r - Return to main menu\n>> ", end="")
            asker = input().strip().lower()

            if asker not in returns_dict:
                print("Invalid input!\n")
            else:
                return returns_dict[asker]


    @staticmethod
    def ask_segment_value(
        data_length:      int,
        segmenting_style: Literal["count", "size"]
    ) -> str|None:

        if segmenting_style == "count":
            string1 = "number of segments"
        elif segmenting_style == "size":
            string1 = "size of a segment"

        while True:
            print(f"Number of samples: {data_length}\n"
                  f"Input a {string1} (type 'r' to return):\n>> ", end="")
            segment_value = input().strip().lower()

            if segment_value == "r":
                return

            if not segment_value.isdigit():
                print("Invalid input!\n")
                continue

            segment_value = int(segment_value)
            if segment_value >= data_length:
                print("Invalid, chosen number is too high\n")
                continue
            elif segment_value <= 1:
                print("Invalid, chosen number is too low\n")
                continue

            return segment_value


    @staticmethod
    def ask_settings_type() -> Literal["data_settings", "sonif_settings"] | None:
        returns_dict = {
            "d": "data_settings",
            "s": "sonif_settings",
            "r": None}

        while True:
            print("Choose settings type (type 'r' to return):\n"
                  "d - Data settings\n"
                  "s - Sonification settings\n>> ", end="")
            asker = input().strip().lower()

            if asker not in returns_dict:
                print("Invalid input!\n")
            else:
                return returns_dict[asker]


    @staticmethod
    def ask_data_settings() -> str | None:
        returns_dict = {
            "an": "auto_normalization_at_load",
            "at": "auto_threshold_at_load",
            "ct": "show_thold_chart",
            "cp": "change_cutting_setting_paa",
            "cd": "change_cutting_setting_dwelltimes",
            "sp": "change_segmenting_setting_paa",
            "sd": "change_segmenting_setting_dwelltimes",
            "se": "change_segmenting_setting_emd",
            "r":   None}

        curr_sett_auto_normal:            bool = Utils.get_val_from_json_fix(Askers.settings_rel_path, "AUTOMATIC_NORMALIZATION_AT_LOAD")
        curr_sett_auto_thold:             bool = Utils.get_val_from_json_fix(Askers.settings_rel_path, "AUTOMATIC_THRESHOLD_AT_LOAD")
        curr_sett_show_thold_chart:       bool = Utils.get_val_from_json_fix(Askers.settings_rel_path, "SHOW_THRESHOLD_ON_CHARTS")
        curr_sett_cut_samples_paa:        bool = Utils.get_val_from_json_fix(Askers.settings_rel_path, "CUT_REMAINDER_SAMPLES_PAA")
        curr_sett_cut_samples_dwelltimes: bool = Utils.get_val_from_json_fix(Askers.settings_rel_path, "CUT_REMAINDER_SAMPLES_DWELLTIMES")
        curr_sett_seg_style_paa:           str = Utils.get_val_from_json_fix(Askers.settings_rel_path, "SEGMENTING_STYLE_PAA")
        curr_sett_seg_style_dwelltimes:    str = Utils.get_val_from_json_fix(Askers.settings_rel_path, "SEGMENTING_STYLE_DWELLTIMES")
        curr_sett_seg_style_emd:           str = Utils.get_val_from_json_fix(Askers.settings_rel_path, "SEGMENTING_STYLE_EMD")

        msg_auto_normal_disable       = "Disable automatic normalization during data loading (currently enabled)"
        msg_auto_normal_enable        = "Enable automatic normalization during data loading (currently disabled)"
        msg_auto_thold_disable        = "Disable automatic calculation of threshold during data loading (currently enabled)"
        msg_auto_thold_enable         = "Enable automatic calculation of threshold during data loading (currently disabled)"
        msg_show_thold_disable        = "Disable showing threshold on charts (currently enabled)"
        msg_show_thold_enable         = "Enable showing threshold on charts (currently disabled)"
        msg_cutting_paa_disable       = "Disable cutting remainder data during PAA (currently enabled)"
        msg_cutting_paa_enable        = "Enable cutting remainder data during PAA (currently disabled)"
        msg_cutting_dtimes_disable    = "Disable cutting remainder data during dwell times conversion (currently enabled)"
        msg_cutting_dtimes_enable     = "Enable cutting remainder data during dwell times conversion (currently disabled)"
        msg_segm_style_paa_tosize     = "size (currently segment count)"
        msg_segm_style_paa_tocount    = "count (currently segment size)"
        msg_segm_style_dtimes_tosize  = "size (currently segment count)"
        msg_segm_style_dtimes_tocount = "count (currently segment size)"
        msg_segm_style_emd_tosize     = "size (currently segment count)"
        msg_segm_style_emd_tocount    = "count (currently segment size)"

        msg_auto_normal = (msg_auto_normal_disable
                           if curr_sett_auto_normal
                           else msg_auto_normal_enable)
        msg_auto_thold = (msg_auto_thold_disable
                          if curr_sett_auto_thold
                          else msg_auto_thold_enable)
        msg_show_thold = (msg_show_thold_disable
                          if curr_sett_show_thold_chart
                          else msg_show_thold_enable)
        msg_cutting_paa = (msg_cutting_paa_disable
                           if curr_sett_cut_samples_paa
                           else msg_cutting_paa_enable)
        msg_cutting_dtimes = (msg_cutting_dtimes_disable
                              if curr_sett_cut_samples_dwelltimes
                              else msg_cutting_dtimes_enable)
        msg_segm_style_paa = (msg_segm_style_paa_tosize
                              if curr_sett_seg_style_paa == "count"
                              else msg_segm_style_paa_tocount
                              if curr_sett_seg_style_paa == "size"
                              else "ERROR")
        msg_segm_style_dtimes = (msg_segm_style_dtimes_tosize
                                 if curr_sett_seg_style_dwelltimes == "count"
                                 else msg_segm_style_dtimes_tocount
                                 if curr_sett_seg_style_dwelltimes == "size"
                                 else "ERROR")
        msg_segm_style_emd = (msg_segm_style_emd_tosize
                                 if curr_sett_seg_style_emd == "count"
                                 else msg_segm_style_emd_tocount
                                 if curr_sett_seg_style_emd == "size"
                                 else "ERROR")

        while True:
            print( "Choose an action:\n"
                  f"an - {msg_auto_normal}\n"
                  f"at - {msg_auto_thold}\n"
                  f"ct - {msg_show_thold}\n"
                  f"cp - {msg_cutting_paa}\n"
                  f"cd - {msg_cutting_dtimes}\n"
                  f"sp - Change segmenting style for PAA to segment {msg_segm_style_paa}\n"
                  f"sd - Change segmenting style for dwell times conversion to segment {msg_segm_style_dtimes}\n"
                  f"se - Change segmenting style for EMD extremes finding {msg_segm_style_emd}\n"
                   "r  - Return to main menu\n>> ", end="")
            asker = input().strip().lower()

            if asker not in returns_dict:
                print("Invalid input!\n")
            else:
                return returns_dict[asker]


    @staticmethod
    def ask_sonif_settings() -> str | None:
        returns_dict = {
            "bl": "change_binary_low_note",
            "bh": "change_binary_high_note",
            "st": "change_similarity_threshold",
            "r":   None}

        curr_sett_binary_low_note:        str = Utils.get_val_from_json_fix(Askers.settings_rel_path, "BINARY_SONIFICATION_LOW_NOTE")
        curr_sett_binary_high_note:       str = Utils.get_val_from_json_fix(Askers.settings_rel_path, "BINARY_SONIFICATION_HIGH_NOTE")
        curr_sett_similarity_threshold: float = Utils.get_val_from_json_fix(Askers.settings_rel_path, "SONIFICATION_SIMILARITY_THRESHOLD")

        while True:
            print( "Choose an action:\n"
                  f"bl - Change low note in binary sonification (currently {curr_sett_binary_low_note})\n"
                  f"bh - Change high note in binary sonification (currently {curr_sett_binary_high_note})\n"
                  f"st - Change similarity threshold (currently {curr_sett_similarity_threshold})\n"
                   "r  - Return to main menu\n>> ", end="")
            asker = input().strip().lower()

            if asker not in returns_dict:
                print("Invalid input!\n")
            else:
                return returns_dict[asker]


    @staticmethod
    def ask_note_binary(
        low_or_high: Literal["low", "high"]
    ) -> str|None:
        available_notes = Utils.get_keys_from_json(Askers.notes_rel_path)
        lowest_note     = available_notes[0]
        highest_note    = available_notes[-1]

        temp_dict_key = "BINARY_SONIFICATION_LOW_NOTE" if low_or_high == "low" else "BINARY_SONIFICATION_HIGH_NOTE"
        current_note  = Utils.get_val_from_json_fix(
            Askers.settings_rel_path,
            temp_dict_key)

        while True:
            print(f"Choose a new {low_or_high} note for binary sonification (currently {current_note})\n"
                  f"Available notes from {lowest_note} to {highest_note}\n"
                   "(type 'r' to return)\n>> ", end="")
            asker = input().strip().upper() #Upper here is crucial!

            if asker in available_notes:
                return asker
            elif asker == "R":
                return
            else:
                print("Invalid input!\n")


    @staticmethod
    def ask_sonif_type(
        bin_available:    bool,
        analog_available: bool
    ) -> Literal["binary", "analog"] | None:
        returns_dict = {
            "b": "binary",
            "a": "analog"
        }

        while True:
            bin_msg    = (
                "b - Sonify binary data..."
                if bin_available
                else "b - Sonify binary data... (UNAVAILABLE)")
            analog_msg = (
                "a - Sonify analog data..."
                if analog_available
                else "a - Sonify analog data... (UNAVAILABLE)")

            print("Choose a method of sonification (type 'r' to return):\n"
                 f"{bin_msg}\n"
                 f"{analog_msg}\n>> ", end="")
            asker = input().strip().lower()

            if asker == "r":
                return
            elif asker not in returns_dict:
                print("Invalid input!\n")
            elif asker in returns_dict:
                if asker == "b":
                    if not bin_available:
                        print("Option unavailable; data has to be converted to binary first.\n\n")
                        continue
                    else:
                        return returns_dict[asker]
                elif asker == "a":
                    if not analog_available:
                        print("Option unavailable; data has to be normalized first.\n\n")
                        continue
                    else:
                        return returns_dict[asker]


    @staticmethod
    def ask_note_duration() -> int | None:
        while True:
            print("Input new note duration (ms):\n"
                  "(type 'r' to return)\n>> ", end="")
            asker = input().strip()

            if asker == "r":
                return
            if not asker.isdigit():
                print("Invalid input.\n")
                continue

            asker = int(asker)
            if asker > 4000:
                print("Duration is too long (max 4000)\n")
                continue
            elif asker < 1:
                print("Duration is too short (min 1)\n")
                continue
            else:
                return asker


    @staticmethod
    def ask_lowest_note_anal(
        current_lowest_note_name:     str,
        highest_lowest_note_possible: str,
        notes:                        list[str]
    ) -> str | None:
        lowest_lowest_note_possible: str = notes[0]
        highest_possible_index = notes.index(highest_lowest_note_possible)
        available_notes = notes[:highest_possible_index+1]
        while True:
            print(f"Choose a new lowest note for analog sonification (currently {current_lowest_note_name})\n"
                  f"Available notes from {lowest_lowest_note_possible} to {highest_lowest_note_possible}\n"
                   "(type 'r' to return)\n>> ", end="")
            asker = input().strip().upper()

            if asker in available_notes:
                return asker
            elif asker == "R":
                return
            else:
                print("Invalid input!\n")


    @staticmethod
    def ask_note_amount(available_notes_count: int) -> int | None:
        min_amount = 5
        max_amount = (30
                      if available_notes_count >= 30
                      else available_notes_count)

        while True:
            print(f"Enter a new amount of notes (value between {min_amount} and {max_amount})\n"
                   "(type 'r' to return)\n>> ", end="")
            asker = input().strip().lower()

            if asker == "r":
                return
            elif not asker.isdigit():
                print("Invalid input.\n\n")

            asker = int(asker)
            if asker < min_amount:
                print("Entered number is too high.\n\n")
                continue
            elif asker > max_amount:
                print("Entered number is too low.\n\n")
                continue

            return asker


    @staticmethod
    def ask_similarity_threshold() -> float:
        min_val = 0.001
        max_val = 0.3

        while True:
            print(f"Enter a new similarity threshold between {min_val} and {max_val}"
                   "(type 'r' to return)\n>> ", end="")
            asker = input().strip().lower()

            if asker == "r":
                return

            try:
                asker = float(asker)
            except (ValueError, TypeError):
                print("Invalid input.\n\n")
                continue

            if asker > max_val:
                print("Number too high.\n\n")
                continue
            if asker < min_val:
                print("Number is probably too low.\n\n")
                continue

            return asker
