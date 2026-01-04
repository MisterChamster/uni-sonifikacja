import os
from tkinter import filedialog
import json
from src.utils import fix_value_in_settingsjson



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
    def ask_segment() -> int|None:
        while True:
            print("Segment data (Pick every n-th line of data. Max 10, optimal 5.)\n"
                  "Press Enter to skip. Input 'exit' to exit program.\n"
                  "n = ", end="")
            asker = input().strip()

            if asker == "":
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
            "p": "apply_paa",
            "n": "normalization",
            "t": "calculate_threshold",
            "c": "show_chart",
            "h": "show_histogram",
            "s": "settings",
            "f": "change_file",
            "exit": "exit"}

        while True:
            print("Choose an action:\n"
                  "x - Reverse data order\n"
                  "y - Reverse data sign\n"
                  "p - Apply PAA downsampling\n"
                  "n - Normalize data\n"
                  "t - Calculate threshold\n"
                  "c - Show chart\n"
                  "h - Show histogram\n"
                  "s - Settings\n"
                  "f - Change file\n"
                  "exit - Exit\n>> ", end="")
            asker = input().strip()

            if asker not in returns_dict:
                print("Invalid input!\n")
            else:
                return returns_dict[asker]


    @staticmethod
    def ask_segments_paa(data_length: int) -> str|None:
        while True:
            print(f"Number of samples: {data_length}")
            print("Input a number of segments (type 'exit' to return):\n>> ", end="")
            segment_count = input().strip()

            if segment_count == "exit":
                return

            if not segment_count.isdigit():
                print("Invalid input!\n")
                continue

            segment_count = int(segment_count)
            if segment_count >= data_length:
                print("Invalid, chosen number is too high\n")
                continue
            elif segment_count <= 1:
                print("Invalid, chosen number is too low\n")
                continue

            return segment_count


    @staticmethod
    def ask_settings() -> str:
        returns_dict = {
            "c":    "change_cutting_setting",
            "exit": "exit"}

        with open("src/settings.json") as f:
            config = json.load(f)
        try:
            cut_string = config["CUT_REMAINDER_STRING"]
        except:
            default: bool = True
            cut_string = default
            fix_value_in_settingsjson("src/settings.json", "CUT_REMAINDER_STRING", default)

        if cut_string:
            cutting_option = "c    - Disable cutting remainder data during PAA (currently enabled)"
        else:
            cutting_option = "c    - Enable cutting remainder data during PAA (currently disabled)"

        while True:
            print( "Choose an action:\n"
                  f"{cutting_option}\n"
                   "exit - Exit\n>> ", end="")
            asker = input().strip()

            if asker not in returns_dict:
                print("Invalid input!\n")
            else:
                return returns_dict[asker]
