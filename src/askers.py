import os
from tkinter import filedialog
from src.utils import Utils



class Askers():
    @staticmethod
    def ask_path_filedialog(node_type: str, message: str) -> str:
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
    def ask_initial_segmentation() -> int|None:
        while True:
            print("Segment data (Pick every n-th line of data. Max 10, optimal 5.)\n"
                  "Press Enter to skip. Input 'exit' to exit program.\n"
                  "n = ", end="")
            asker = input().strip().lower()

            if not asker:
                return 1
            elif asker == "exit":
                return
            elif not asker.isdigit():
                print("Incorrect input.\n\n")
            else:
                asker = int(asker)
                if asker <= 1:
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
            "p": "apply_paa",
            "b": "convert_to_bin",
            "d": "convert_to_dwelltimes",
            "c": "show_chart",
            "h": "show_histogram",
            "s": "settings",
            "o": "original_data",
            "f": "change_file",
            "exit": "exit"}

        while True:
            print("Choose an action:\n"
                  "x - Reverse data order\n"
                  "y - Reverse data sign\n"
                  "n - Normalize data\n"
                  "t - Calculate threshold\n"
                  "p - Apply PAA downsampling\n"
                  "b - Convert data to binary\n"
                  "d - Convert data to dwell times\n"
                  "c - Show chart\n"
                  "h - Show histogram\n"
                  "s - Settings\n"
                  "o - Revert to original data set\n"
                  "f - Change file\n"
                  "exit - Exit\n>> ", end="")
            asker = input().strip().lower()

            if asker not in returns_dict:
                print("Invalid input!\n")
            else:
                return returns_dict[asker]


    @staticmethod
    def ask_segment_value(data_length: int, segmenting_style: str) -> str|None:
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
    def ask_settings() -> str:
        returns_dict = {
            "cp":   "change_cutting_setting_paa",
            "cd":   "change_cutting_setting_dwelltimes",
            "sp":   "change_segmenting_setting_paa",
            "sd":   "change_segmenting_setting_dwelltimes",
            "exit": "exit"}

        # Get current settings from settings.json
        cut_string_paa          = Utils.get_val_from_settings_fix("src/settings.json",
                                                                  "CUT_REMAINDER_SAMPLES_PAA",
                                                                  True)
        cut_string_dwelltimes   = Utils.get_val_from_settings_fix("src/settings.json",
                                                                  "CUT_REMAINDER_SAMPLES_DWELLTIMES",
                                                                  True)
        segment_style_paa       = Utils.get_val_from_settings_fix("src/settings.json",
                                                                  "SEGMENTING_STYLE_PAA",
                                                                  "count")
        segment_style_dwelltimes = Utils.get_val_from_settings_fix("src/settings.json",
                                                                  "SEGMENTING_STYLE_DWELLTIMES",
                                                                  "size")

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
                   "exit - Exit\n>> ", end="")
            asker = input().strip().lower()

            if asker not in returns_dict:
                print("Invalid input!\n")
            else:
                return returns_dict[asker]
