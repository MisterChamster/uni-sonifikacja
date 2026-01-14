import json
from typing import Literal
from datetime          import datetime



class Utils():
    @staticmethod
    def save_value_to_settings(
        adress:   str,
        json_key: str,
        json_val: bool|str|int|float
    ) -> None:

        with open(adress) as f:
            config = json.load(f)

        config[json_key] = json_val
        with open(adress, "w") as f:
            json.dump(config, f, indent=2)


    @staticmethod
    def fix_value_in_settings(
        adress:      str,
        json_key:    str,
        default_val: bool|str|int|float
    ) -> None:

        with open(adress) as f:
            config = json.load(f)

        if json_key not in config.keys():
            print(f"[WARNING] Key value '{json_key}' could not be found in {adress}. Resorting to default value ('{default_val}').\nFixing {adress}...")
            try:
                Utils.save_value_to_settings(adress, json_key, default_val)
                print(f"{json_key} has been fixed in {adress}")
            except Exception as e:
                print(f"{json_key} could not have been fixed in {adress}\n{e}")
        return


    @staticmethod
    def get_val_from_json(
        adress:   str,
        json_key: str
    ) -> str|bool|int|float:

        with open(adress) as f:
            config = json.load(f)

        temp = config[json_key]
        return temp


    @staticmethod
    def get_val_from_json_fix(
        adress:      str,
        json_key:    Literal[
            "AUTOMATIC_THRESHOLD_AT_LOAD",
            "CUT_REMAINDER_SAMPLES_PAA",
            "CUT_REMAINDER_SAMPLES_DWELLTIMES",
            "SEGMENTING_STYLE_PAA",
            "SEGMENTING_STYLE_DWELLTIMES",
            "SAMPLE_RATE",
            "BINARY_SONIFICATION_LOW_NOTE",
            "BINARY_SONIFICATION_HIGH_NOTE",
            "BINARY_SONIFICATION_NOTE_DURATION_MILIS",
            "ANAL_SONIFICATION_NOTE_DURATION_MILIS",
            "ANAL_SONIFICATION_AMOUNT_OF_USED_NOTES",
            "ANAL_SONIFICATION_LOWEST_NOTE"],
        default_val: str|bool|int|float = None
    ) -> str|bool|int|float:

        if not default_val:
            default_settings_dict = {
                "AUTOMATIC_THRESHOLD_AT_LOAD":             True,
                "CUT_REMAINDER_SAMPLES_PAA":               True,
                "CUT_REMAINDER_SAMPLES_DWELLTIMES":        True,
                "SEGMENTING_STYLE_PAA":                   "count",
                "SEGMENTING_STYLE_DWELLTIMES":            "count",
                "SAMPLE_RATE":                             44100,
                "BINARY_SONIFICATION_LOW_NOTE":           "D3",
                "BINARY_SONIFICATION_HIGH_NOTE":          "A4",
                "BINARY_SONIFICATION_NOTE_DURATION_MILIS": 300,
                "ANAL_SONIFICATION_NOTE_DURATION_MILIS":   300,
                "ANAL_SONIFICATION_AMOUNT_OF_USED_NOTES":  20,
                "ANAL_SONIFICATION_LOWEST_NOTE":          "D3"}
            default_val = default_settings_dict[json_key]

        try:
            temp = Utils.get_val_from_json(adress, json_key)
            return temp
        except:
            Utils.fix_value_in_settings(adress, json_key, default_val)
            return default_val


    @staticmethod
    def change_setting_to_opposite(
        adress:      str,
        json_key:    str
    ) -> None:
        setting_val = Utils.get_val_from_json_fix(
            adress,
            json_key)

        if isinstance(setting_val, bool):
            setting_val = not setting_val
        elif setting_val in ["size", "count"]:
            setting_val = "size" if setting_val == "count" else "size"
        else:
            raise ValueError("ERROR: Incorrect value in settings.json")

        Utils.save_value_to_settings(adress, json_key, setting_val)
        return


    @staticmethod
    def get_keys_from_json(rel_adress: str) -> list[str]:
        with open(rel_adress) as f:
            dict_from_json = json.load(f)

        return list(dict_from_json.keys())


    @staticmethod
    def get_dict_from_json(rel_adress: str) -> dict[str]:
        with open(rel_adress) as f:
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
