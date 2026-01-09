# import pandas as pd
# from math import floor
import json



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
        json_key:    str,
        default_val: str|bool|int|float
    ) -> str|bool|int|float:

        try:
            temp = Utils.get_val_from_json(adress, json_key)
            return temp
        except:
            Utils.fix_value_in_settings(adress, json_key, default_val)
            return default_val


    @staticmethod
    def change_setting_to_opposite(
        adress:      str,
        json_key:    str,
        default_val: str|bool
    ) -> None:

        setting_val = Utils.get_val_from_json_fix(
            adress,
            json_key,
            default_val)

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
        return dict_from_json.keys()


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
