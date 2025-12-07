import os
from tkinter import filedialog



class Askers():
    def ask_path_filedialog(type, message) -> str:
        original_path = os.getcwd()
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        os.chdir(desktop_path)

        sel_path = ""
        if type == "f":
            sel_path = filedialog.askopenfilename(title=message)
        elif type == "d":
            sel_path = filedialog.askdirectory(title=message)

        os.chdir(original_path)
        return sel_path


    def ask_segment() -> int:
        while True:
            print("Segment data (Pick every n-th line of data. Max 10, optimal 5.)\n"
                  "Press Enter to skip.\n"
                  "n = ", end="")
            asker = input().strip()

            if asker == "":
                return None
            elif not asker.isdigit():
                print("Incorrect input.\n\n")
            else:
                asker = int(asker)
            if asker <= 1:
                return None
            elif asker > 10:
                print("Input too high.\n\n")
            else:
                return asker


    def ask_normalize() -> bool:
        rets_dict = {"y": True,
                     "n": False}

        while True:
            print("Do You want to normalize the data? (y/n)\n"
                  ">> ", end="")
            asker = input().strip()

            if asker in rets_dict:
                return rets_dict[asker]
            else:
                print("Incorrect input.\n\n")

    def ask_action():
        returns_dict = {
            "n": "normalisation",
            "t": "calculate_threshold",
            "c": "show_chart",
            "h": "show_histogram",
            "e": "exit"}

        while True:
            print("Choose an action:\n"
                  "n - Normalisation\n"
                  "t - Calculating threshold\n"
                  "c - Showing chart\n"
                  "h - Showing histogram\n"
                  "e - Exit\n>> ", end="")
            asker = input().strip()

            if asker not in returns_dict:
                print("Invalid input!\n")
            else:
                return returns_dict[asker]
