import json
from pathlib import Path
from typing   import Literal
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np



class Utils():
    """
    Container class for various functions.

    Attributes:
        settings_path (Path): Stores path to settings.json.
        notes_path (Path): Stores path to notes.json.
    """

    @staticmethod
    def save_value_to_settings(
        json_key: str,
        json_val: bool|str|int|float
    ) -> None:
        """
        Save value with key to settings.json.

        Args:
            json_key (str): Key for value to be saved.
            json_val (bool|str|int|float): Value to be saved.
        """

        with open(Utils.settings_path) as f:
            config = json.load(f)

        config[json_key] = json_val
        with open(Utils.settings_path, "w") as f:
            json.dump(config, f, indent=2)


    @staticmethod
    def fix_value_in_json(
        adress:     Path,
        json_key:    str,
        default_val: bool|str|int|float
    ) -> None:
        """
        Fix a value in json if it's broken.

        Chcecks if a key is present in settings. If not, 
        adds it with default value given.

        Args:
            adress (Path): Path to json file.
            json_key (str): Key to fix.
            default_val (bool|str|int|float): Value for key if fixing is needed.
        """

        with open(adress) as f:
            config = json.load(f)

        if json_key not in config.keys():
            print(f"[WARNING] Key value '{json_key}' could not be found in {adress}. Resorting to default value ('{default_val}').\nFixing {adress}...")
            try:
                Utils.save_value_to_settings(json_key, default_val)
                print(f"{json_key} has been fixed in {adress}")
            except Exception as e:
                print(f"{json_key} could not have been fixed in {adress}\n{e}")
        return


    @staticmethod
    def get_val_from_json(
        adress:  Path,
        json_key: str
    ) -> str|bool|int|float:
        """
        Get value from json file for given key.

        Args:
            adress (str): Path to json file.
            json_key (str): Key to get value from.
        """

        with open(adress) as f:
            config = json.load(f)

        temp = config[json_key]
        return temp


    @staticmethod
    def get_val_from_settings_fix(
        json_key: Literal[
            "AUTOMATIC_NORMALIZATION_AT_LOAD",
            "AUTOMATIC_THRESHOLD_AT_LOAD",
            "SHOW_THRESHOLD_ON_CHARTS",
            "CUT_REMAINDER_SAMPLES_PAA",
            "CUT_REMAINDER_SAMPLES_DWELLTIMES",
            "SEGMENTING_STYLE_PAA",
            "SEGMENTING_STYLE_DWELLTIMES",
            "EMD_CONSIDER_IMFS_FROM",
            "SAMPLE_RATE",
            "BINARY_SONIF_LOW_NOTE",
            "BINARY_SONIF_HIGH_NOTE",
            "BINARY_SONIF_NOTE_DURATION_MILIS",
            "ANAL_SONIF_NOTE_DURATION_MILIS",
            "ANAL_SONIF_AMOUNT_OF_USED_NOTES",
            "ANAL_SONIF_LOWEST_NOTE",
            "SONIF_SIMILARITY_THRESHOLD"],
        default_val: str|bool|int|float = None
    ) -> str|bool|int|float:
        """
        Get val from settings, fix with automatic if needed.

        Attempts to get a value from settings for given literal 
        key. If fails, attempts to fix it with pre defined values.

        Args:
            json_key (str): A literal key to get values from.
            default_val (str|bool|int|float): Optional value for assigning non-predefined values.

        Returns:
            Value read from settings or default if there were problems.
        """

        try:
            temp = Utils.get_val_from_json(Utils.settings_path, json_key)
            return temp

        except:
            if not default_val:
                default_settings_dict = {
                    "AUTOMATIC_NORMALIZATION_AT_LOAD":  True,
                    "AUTOMATIC_THRESHOLD_AT_LOAD":      True,
                    "SHOW_THRESHOLD_ON_CHARTS":         True,
                    "CUT_REMAINDER_SAMPLES_PAA":        True,
                    "CUT_REMAINDER_SAMPLES_DWELLTIMES": True,
                    "SEGMENTING_STYLE_PAA":            "count",
                    "SEGMENTING_STYLE_DWELLTIMES":     "count",
                    "EMD_CONSIDER_IMFS_FROM":           10,
                    "SAMPLE_RATE":                      44100,
                    "BINARY_SONIF_LOW_NOTE":           "D3",
                    "BINARY_SONIF_HIGH_NOTE":          "A4",
                    "BINARY_SONIF_NOTE_DURATION_MILIS": 300,
                    "ANAL_SONIF_NOTE_DURATION_MILIS":   300,
                    "ANAL_SONIF_AMOUNT_OF_USED_NOTES":  20,
                    "ANAL_SONIF_LOWEST_NOTE":          "D3",
                    "SONIF_SIMILARITY_THRESHOLD":       0.03}
                default_val = default_settings_dict[json_key]

            Utils.fix_value_in_json(Utils.settings_path, json_key, default_val)
            return default_val


    @staticmethod
    def change_setting_to_opposite(json_key: str) -> None:
        """
        Change binary settings to opposite.

        Changes two-state settings to opposite to what is 
        currently set. Is able to change bool values, 
        size/count and fixed/user.

        Args:
            json_key: Key to change the value of.
        """
        setting_val = Utils.get_val_from_settings_fix(json_key)

        if isinstance(setting_val, bool):
            setting_val = not setting_val
        elif setting_val in ["size", "count"]:
            setting_val = "size" if setting_val == "count" else "count"
        elif setting_val in ["fixed", "user"]:
            setting_val = "fixed" if setting_val == "user" else "user"
        else:
            raise ValueError("[ERROR] Code is written badly. Incorrect value in settings.json")

        Utils.save_value_to_settings(json_key, setting_val)
        return


    @staticmethod
    def get_keys_from_json(json_adress: Path) -> list[str]:
        """
        Get keys from json file.

        Args:
            json_adress (Path): Adress of the json file.

        Returns:
            List of keys from chosen json file.
        """
        with open(json_adress) as f:
            dict_from_json = json.load(f)

        return list(dict_from_json.keys())


    @staticmethod
    def get_dict_from_json(json_adress: Path) -> dict[str]:
        with open(json_adress) as f:
            dict_from_json = json.load(f)

        return dict_from_json


    @staticmethod
    def human_read_milis(milis: int) -> str:
        seconds = milis // 1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        parts = []
        if hours:
            parts.append(f"{hours} hour(s)")
        if minutes:
            parts.append(f"{minutes} minute(s)")
        if seconds:
            parts.append(f"{seconds} second(s)")

        return ", ".join(parts) or "0 seconds"


    @staticmethod
    def get_curr_time_to_name() -> str:
        currtime: datetime   = datetime.now()
        currtime_string: str = currtime.strftime("%Y-%m-%d_%H:%M:%S")
        return currtime_string


    @staticmethod
    def _is_anal_possible(
        notes:        list[str],
        lowest_note:  str,
        notes_amount: int
    ) -> bool:
        if not lowest_note in notes:
            return False

        lowest_note_index: int  = notes.index(lowest_note)
        highest_note_index: int = lowest_note_index + notes_amount - 1
        if highest_note_index + 1 > len(notes):
            return False

        return True


    @staticmethod
    def _get_highest_note_anal(
        notes:        list[str],
        lowest_note:  str,
        notes_amount: int
    ) -> str:
        lowest_note_index: int  = notes.index(lowest_note)
        highest_note_index: int = lowest_note_index + notes_amount - 1
        return notes[highest_note_index]


    @staticmethod
    def get_highest_note_anal_safe(
        notes:        list[str],
        lowest_note:  str,
        notes_amount: int
    ) -> str | None:
        """
        Checks if it is possible to get the highest note.
        Then, calculates the highest note name and returns it.
        """
        is_anal_possible = Utils._is_anal_possible(
            notes,
            lowest_note,
            notes_amount)

        if not is_anal_possible:
            return

        highest_note_name = Utils._get_highest_note_anal(
            notes,
            lowest_note,
            notes_amount)
        return highest_note_name


    @staticmethod
    def get_highest_lowest_note_possible_for_amount(
        notes:        list[str],
        notes_amount: int
    ) -> str:
        """
        Return the highest possible lowest note that can be selected when choosing
        a fixed number of notes from an ordered note list.
        """
        highest_lowest_note_index = len(notes) - notes_amount
        highest_lowest_note       = notes[highest_lowest_note_index]
        return highest_lowest_note


    @staticmethod
    def get_notes_used_list(
        notes:        list[str],
        lowest_note:  str,
        notes_amount: int
    ) -> list[str]:
        lowest_index = notes.index(lowest_note)
        notes = notes[lowest_index:]
        notes = notes[:notes_amount]
        return notes


    @staticmethod
    def draw_tone(tone: np.ndarray) -> None:
        """
        Plots a soundwave on a chart.

        Args:
            tone (np.ndarray): Soundwave to draw.
        """
        plt.figure()
        plt.plot(tone)
        plt.xlabel("Sample")
        plt.ylabel("Amplitude")
        plt.title("Soundwave")
        plt.show()
