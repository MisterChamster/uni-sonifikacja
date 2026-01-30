import os
from pathlib import Path
from tkinter import filedialog
from typing  import Literal

from src.utils import Utils



class Askers():
    """
    Container class for asker functions.

    Askers are static methods that prompt user to input a value. In most cases 
    they can come in form of a menu or a piece of code inquiring a value to 
    assign to a variable.

    Attributes:
        settings_path (Path): Path to a settings file.
        notes_path (Path): Path to a notes file.
    """


    @staticmethod
    def ask_path_filedialog(starting_path: (str)) -> str:
        """
        Open file dialogbox and get txt/csv file.

        Opens a file dialog box that propmpts user to choose a txt or csv file, 
        starting on a starting_path path.

        Args:
            starting_path (str): Path where dialog box opens.

        Returns:
            Path of the chosen file.
        """
        original_path = os.getcwd()
        os.chdir(starting_path)

        sel_path = filedialog.askopenfilename(
            title="Choose a txt or csv file",
            filetypes=[
                ("TXT files", "*.txt"),
                ("CSV files", "*.csv")])

        os.chdir(original_path)
        return sel_path


    @staticmethod
    def ask_downsampling(is_initial: bool = False) -> int|None:
        """
        Get downsampling n value from user.

        Asks user to choose n value for downsampling that ranges from 1 to 10. 
        If user doesn't want to downsample, returns None instead.

        Args:
            is_initial (bool): Determines if menu is for initial segmentation or not.

        Returns:
            n value for downsampling in (1, 10) or None if not chosen.
        """
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
    def ask_action() -> Literal[
        "process_data",
        "sonify",
        "show_chart",
        "show_histogram",
        "settings",
        "original_data",
        "change_file",
        "exit"]:
        """
        Get main menu action.

        Returns:
            Actions in forms of pre-defined strings.
        """
        returns_dict = {
            "p": "process_data",
            "s": "sonify",
            "c": "show_chart",
            "h": "show_histogram",
            "t": "settings",
            "o": "original_data",
            "f": "change_file",
            "exit": "exit"}

        while True:
            print("Choose an action:\n"
                  "p - Process data...\n"
                  "s - Sonify data...\n"
                  "c - Show chart\n"
                  "h - Show histogram\n"
                  "t - Settings...\n"
                  "o - Revert to original data set\n"
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
    ) -> Literal[
        "reverse_order",
        "reverse_sign",
        "normalization",
        "calculate_threshold",
        "downsample_data",
        "apply_paa",
        "convert_to_bin",
        "convert_to_dwelltimes",
        "convert_to_dwelltimes_reduced",
        "appy_emd"] | None:
        """
        Get processing menu action.

        Returns:
            Actions in forms of pre-defined strings or None if returning.
        """
        returns_dict = {
            "x": "reverse_order",
            "y": "reverse_sign",
            "n": "normalization",
            "t": "calculate_threshold",
            "d": "downsample_data",
            "p": "apply_paa",
            "b": "convert_to_bin",
            "i": "convert_to_dwelltimes",
            "c": "convert_to_dwelltimes_reduced",
            "e": "appy_emd",
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
                  "i - Convert data to dwell times\n"
                  "c - Convert data to reduced dwell times\n"
                  "e - Apply EMD method\n"
                  "r - Return to main menu\n>> ", end="")
            asker = input().strip().lower()

            if asker not in returns_dict:
                print("Invalid input!\n")
            else:
                return returns_dict[asker]


    @staticmethod
    def ask_new_imfs_from() -> int | None:
        """
        Get number of IMF to start displaying from.

        Returns:
            Number of IMF in (min_num, max_num) or None if not chosen.
        """
        min_num = 1
        max_num = 20

        while True:
            print(f"Enter a number from which IMFs will be shown (between {min_num} and {max_num})\n"
                   "(enter 'r' to return)\n>> ", end="")
            asker = input().strip().lower()

            if asker == "r":
                return
            if not asker.isdigit():
                print("Invalid input!\n")
                continue
            asker = int(asker)

            if asker < min_num:
                print("Value is too low.\n")
                continue
            if asker > max_num:
                print("Value is too high.\n")
                continue

            return asker


    @staticmethod
    def ask_imf_num(lowest: int, highest: int) -> int | None:
        """
        Get number of IMF to pick.

        Args:
            lowest (int): Lowest possible IMF to pick.
            highest (int): Highest possible IMF to pick.

        Returns:
            Number of IMF in (min_num, max_num) or None if not chosen.
        """
        while True:
            print("Enter a number of IMF You want to set as new data\n"
                  "(type 'r' to return)\n>> ", end="")
            asker = input().strip().lower()

            if asker == 'r':
                return

            if not asker.isdigit():
                print("Invalid input!\n")
                continue

            asker = int(asker)
            if asker < lowest:
                print("Value is too low.\n")
                continue
            if asker > highest:
                print("Value is too high.\n")
                continue

            return asker


    @staticmethod
    def ask_segment_value(
        data_length:      int,
        segmenting_style: Literal["count", "size"]
    ) -> int | None:
        """
        Get segmenting value from user.

        Asks user to input a segmenting value. Prints depend on what style 
        of segmenting is chosen. User input is checked to be in a correct 
        range.

        Args:
            data_length (int): Length of the data to be segmented.
            segmenting_style (str): Type of segmentation to be performed.

        Returns:
            Value of a segment (length or size) or None if not chosen.
        """

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
        """
        Get settings type menu action.

        Returns:
            Actions in forms of pre-defined strings or None if returning.
        """
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
    def ask_data_settings() -> Literal[
        "auto_normalization_at_load",
        "auto_threshold_at_load",
        "show_thold_chart",
        "change_cutting_setting_paa",
        "change_cutting_setting_dwelltimes",
        "change_segmenting_setting_paa",
        "change_segmenting_setting_dwelltimes",
        "change_imfs_from"
    ] | None:
        """
        Get data settings menu action.

        Returns:
            Actions in forms of pre-defined strings or None if returning.
        """
        returns_dict = {
            "an": "auto_normalization_at_load",
            "at": "auto_threshold_at_load",
            "ct": "show_thold_chart",
            "cp": "change_cutting_setting_paa",
            "cd": "change_cutting_setting_dwelltimes",
            "sp": "change_segmenting_setting_paa",
            "sd": "change_segmenting_setting_dwelltimes",
            "if": "change_imfs_from",
            "r":   None}

        curr_sett_auto_normal:            bool = Utils.get_val_from_json_fix(Askers.settings_path, "AUTOMATIC_NORMALIZATION_AT_LOAD")
        curr_sett_auto_thold:             bool = Utils.get_val_from_json_fix(Askers.settings_path, "AUTOMATIC_THRESHOLD_AT_LOAD")
        curr_sett_show_thold_chart:       bool = Utils.get_val_from_json_fix(Askers.settings_path, "SHOW_THRESHOLD_ON_CHARTS")
        curr_sett_cut_samples_paa:        bool = Utils.get_val_from_json_fix(Askers.settings_path, "CUT_REMAINDER_SAMPLES_PAA")
        curr_sett_cut_samples_dwelltimes: bool = Utils.get_val_from_json_fix(Askers.settings_path, "CUT_REMAINDER_SAMPLES_DWELLTIMES")
        curr_sett_seg_style_paa:           str = Utils.get_val_from_json_fix(Askers.settings_path, "SEGMENTING_STYLE_PAA")
        curr_sett_seg_style_dwelltimes:    str = Utils.get_val_from_json_fix(Askers.settings_path, "SEGMENTING_STYLE_DWELLTIMES")
        curr_sett_imfs_from:               int = Utils.get_val_from_json_fix(Askers.settings_path, "EMD_CONSIDER_IMFS_FROM")

        msg_to_size  = "size (currently segment count)"
        msg_to_count = "count (currently segment size)"
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
        msg_segm_style_paa_tosize     = msg_to_size
        msg_segm_style_paa_tocount    = msg_to_count
        msg_segm_style_dtimes_tosize  = msg_to_size
        msg_segm_style_dtimes_tocount = msg_to_count

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

        while True:
            print( "Choose an action:\n"
                  f"an - {msg_auto_normal}\n"
                  f"at - {msg_auto_thold}\n"
                  f"ct - {msg_show_thold}\n"
                  f"cp - {msg_cutting_paa}\n"
                  f"cd - {msg_cutting_dtimes}\n"
                  f"sp - Change segmenting style for PAA to segment {msg_segm_style_paa}\n"
                  f"sd - Change segmenting style for dwell times conversion to segment {msg_segm_style_dtimes}\n"
                  f"if - Change starting number of imfs shown (currently {curr_sett_imfs_from})\n"
                   "r  - Return to main menu\n>> ", end="")
            asker = input().strip().lower()

            if asker not in returns_dict:
                print("Invalid input!\n")
            else:
                return returns_dict[asker]


    @staticmethod
    def ask_sonif_settings() -> Literal[
        "change_binary_low_note",
        "change_binary_high_note",
        "change_similarity_threshold"] | None:
        """
        Get sonification settings menu action.

        Returns:
            Actions in forms of pre-defined strings or None if returning.
        """
        returns_dict = {
            "bl": "change_binary_low_note",
            "bh": "change_binary_high_note",
            "st": "change_similarity_threshold",
            "r":   None}

        curr_sett_binary_low_note:        str = Utils.get_val_from_json_fix(Askers.settings_path, "BINARY_SONIF_LOW_NOTE")
        curr_sett_binary_high_note:       str = Utils.get_val_from_json_fix(Askers.settings_path, "BINARY_SONIF_HIGH_NOTE")
        curr_sett_similarity_threshold: float = Utils.get_val_from_json_fix(Askers.settings_path, "SONIF_SIMILARITY_THRESHOLD")

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
    ) -> str | None:
        """
        Get high or low note for binary sonification.

        Asks user to input a low or high note name depending on argument. 
        Value is checked if exists in notes.json.

        Args:
            low_or_high (str): Low or high note for specific prints.

        Returns:
            Note name of lowest/highest note or None if not chosen.
        """
        available_notes = Utils.get_keys_from_json(Askers.notes_path)
        lowest_note     = available_notes[0]
        highest_note    = available_notes[-1]

        temp_dict_key = ("BINARY_SONIF_LOW_NOTE"
                         if low_or_high == "low"
                         else "BINARY_SONIF_HIGH_NOTE")
        current_note  = Utils.get_val_from_json_fix(
            Askers.settings_path,
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
        """
        Get sonification type menu action.

        Asks user to pick sonification type. Displays messages when it is 
        not available. Picking unavailabe message makes program display 
        the reason why it's not available.

        Args:
            bin_available (bool): Informs if binary sonification is available for choosing.
            analog_available (bool): Informs if analog sonification is available for choosing.

        Returns:
            Actions in forms of pre-defined strings or None if returning.
        """
        returns_dict = {
            "b": "binary",
            "a": "analog"}

        while True:
            bin_msg = (
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
        """
        Get duration of a note in ms.

        Asks user how much miliseconds a single note should last. 
        Value is then checked if it is present within a range of acceptable 
        answers.

        Returns:
            Number of miliseconds that every sample lasts in output audio file or None if not chosen.
        """
        lowest = 1
        highest = 4000
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
            if asker > highest:
                print(f"Duration is too long (max {highest})\n")
                continue
            elif asker < lowest:
                print(f"Duration is too short (min {lowest})\n")
                continue
            return asker


    @staticmethod
    def ask_lowest_note_anal(
        current_lowest_note_name:     str,
        highest_lowest_note_possible: str,
        notes:                        list[str]
    ) -> str | None:
        """
        Get lowest note for analog sonification from user.

        Calculates a range of notes that are possible to choose from, 
        then prompts user to choose one. Checks if input is within range.

        Args:
            current_lowest_note_name (str): Current lowest note name.
            highest_lowest_note_possible (str): Highest lowest note name possible.
            notes (list[str]): All notes available for sonification.

        Returns:
            Lowest note for analog sonification or None if not chosen.
        """
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
        """
        Get amount of notes for analog sonification from user.

        Asks user for the amount of notes to be used in analog sonification. 
        Checks if value fits within a specified range.

        Args:
            available_notes_count (int): Upper note threshold (just in case).

        Returns:
            Amount of notes to be used in analog sonification or None if not chosen.
        """
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
        """
        Get similarity threshold from user.

        Asks user for similarity threshold for note cutting during sonification. 
        Checks if value fits within a specified range.

        Returns:
            Similarity threshold for note cutting during sonification.
        """
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
