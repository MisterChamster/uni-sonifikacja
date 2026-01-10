import os
from tkinter import filedialog
from typing import Literal
from src.utils import Utils



class Askers():
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
    def ask_segmentation(is_initial: bool = False) -> int|None:
        stroing = (" Input 'exit' to exit program."
                   if is_initial
                   else "")

        while True:
            print("Segment data (Pick every n-th line of data)\n"
                  "Max value is 10, but highest reasonable is 5.\n"
                  f"Press Enter to skip.{stroing}\n"
                  "n = ", end="")
            asker = input().strip().lower()

            if not asker:
                return 1
            if asker == "exit" and is_initial:
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
            "x": "reverse_order",
            "y": "reverse_sign",
            "n": "normalization",
            "t": "calculate_threshold",
            "e": "segment_data",
            "p": "apply_paa",
            "b": "convert_to_bin",
            "d": "convert_to_dwelltimes",
            "o": "original_data",
            "i": "sonify",
            "c": "show_chart",
            "h": "show_histogram",
            "s": "settings",
            "f": "change_file",
            "exit": "exit"}

        while True:
            print("Choose an action:\n"
                  "x - Reverse data order\n"
                  "y - Reverse data sign\n"
                  "n - Normalize data\n"
                  "t - Calculate threshold\n"
                  "e - Segment data\n"
                  "p - Apply PAA downsampling\n"
                  "b - Convert data to binary\n"
                  "d - Convert data to dwell times\n"
                  "o - Revert to original data set\n"
                  "i - Sonify data...\n"
                  "c - Show chart\n"
                  "h - Show histogram\n"
                  "s - Settings...\n"
                  "f - Change file\n"
                  "exit - Exit\n>> ", end="")
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
            print(f"Number of samples: {data_length}")
            print(f"Input a {string1} (type 'exit' to return):\n>> ", end="")
            segment_value = input().strip().lower()

            if segment_value == "exit":
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
    def ask_settings(settings_rel_adress: str) -> str:
        returns_dict = {
            "cp":   "change_cutting_setting_paa",
            "cd":   "change_cutting_setting_dwelltimes",
            "sp":   "change_segmenting_setting_paa",
            "sd":   "change_segmenting_setting_dwelltimes",
            "bl":   "change_binary_low_note",
            "bh":   "change_binary_high_note",
            "exit": "exit"}

        # Get current settings from settings.json
        cut_string_paa          = Utils.get_val_from_json_fix(
            settings_rel_adress,
            "CUT_REMAINDER_SAMPLES_PAA",
            True)
        cut_string_dwelltimes   = Utils.get_val_from_json_fix(
            settings_rel_adress,
            "CUT_REMAINDER_SAMPLES_DWELLTIMES",
            True)
        segment_style_paa       = Utils.get_val_from_json_fix(
            settings_rel_adress,
            "SEGMENTING_STYLE_PAA",
            "count")
        segment_style_dwelltimes = Utils.get_val_from_json_fix(
            settings_rel_adress,
            "SEGMENTING_STYLE_DWELLTIMES",
            "size")
        binary_low_note = Utils.get_val_from_json_fix(
            settings_rel_adress,
            "BINARY_SONIFICATION_LOW_NOTE",
            "D3")
        binary_high_note = Utils.get_val_from_json_fix(
            settings_rel_adress,
            "BINARY_SONIFICATION_HIGH_NOTE",
            "A4")

        if cut_string_paa:
            cutting_option_paa = "Disable cutting remainder data during PAA (currently enabled)"
        else:
            cutting_option_paa = "Enable cutting remainder data during PAA (currently disabled)"

        if cut_string_dwelltimes:
            cutting_option_dwelltimes = "Disable cutting remainder data during dwell times conversion (currently enabled)"
        else:
            cutting_option_dwelltimes = "Enable cutting remainder data during dwell times conversion (currently disabled)"

        if segment_style_paa == "count":
            segmenting_style_paa = "size (currently segment count)"
        elif segment_style_paa == "size":
            segmenting_style_paa = "count (currently segment size)"

        if segment_style_dwelltimes == "count":
            segmenting_style_dwelltimes = "size (currently segment count)"
        elif segment_style_dwelltimes == "size":
            segmenting_style_dwelltimes = "count (currently segment size)"


        while True:
            print( "Choose an action:\n"
                  f"cp   - {cutting_option_paa}\n"
                  f"cd   - {cutting_option_dwelltimes}\n"
                  f"sp   - Change segmenting style for PAA to segment {segmenting_style_paa}\n"
                  f"sd   - Change segmenting style for dwell times conversion to segment {segmenting_style_dwelltimes}\n"
                  f"bl   - Change low note in binary sonification (currently {binary_low_note})\n"
                  f"bh   - Change high note in binary sonification (currently {binary_high_note})\n"
                   "exit - Exit\n>> ", end="")
            asker = input().strip().lower()

            if asker not in returns_dict:
                print("Invalid input!\n")
            else:
                return returns_dict[asker]


    @staticmethod
    def ask_note(
        notes_rel_adress: str,
        low_or_high:      Literal["low", "high"]
    ) -> str|None:
        available_notes = Utils.get_keys_from_json(notes_rel_adress)
        lowest_note = available_notes[0]
        highest_note = available_notes[-1]

        temp_dict_key = "BINARY_SONIFICATION_LOW_NOTE" if low_or_high == "low" else "BINARY_SONIFICATION_HIGH_NOTE"
        temp_default  = "D3" if low_or_high == "low" else "A4"
        current_note  = Utils.get_val_from_json_fix(
            "src/settings.py",
            temp_dict_key,
            temp_default)
        main_message = f"Choose a new {low_or_high} note for binary sonification (currently {current_note})"

        while True:
            print(main_message)
            print(f"Available notes from {lowest_note} to {highest_note}")
            print("(type 'exit' to exit)\n>> ", end="")
            asker = input().strip().upper() #Upper here is crucial!

            if asker in available_notes:
                return asker
            elif asker == "EXIT":
                return
            else:
                print("Invalid input!\n")


    @staticmethod
    def ask_sonif_type(
        bin_available:    bool,
        analog_available: bool
    ) -> Literal["binary", "analog", None]:
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

            print("Choose a method of sonification (type 'exit' to exit):")
            print(bin_msg)
            print(analog_msg)
            print(">> ", end="")
            asker = input().strip().lower()

            if asker == "exit":
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
                        #COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE
                        # COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE COME_BACK_HER
                        #COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE
                        # COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE COME_BACK_HER
                        print("Option unavailable; FOR A REASON????????????.\n\n")
                        continue
                    else:
                        return returns_dict[asker]


    @staticmethod
    def ask_note_duration() -> int|None:
        while True:
            print("Input new note duration (ms):")
            print("(type 'exit' to exit)\n>> ", end="")
            asker = input().strip()

            if asker == "exit":
                return
            if not asker.isdigit():
                print("Invalid input.\n")
                continue

            asker = int(asker)
            if asker > 4000:
                print("Number is too big (max 4000)\n")
                continue
            else:
                return asker
