# import pandas as pd
# from math import floor
import json



class Utils():
    @staticmethod
    def save_value_to_settings(adress: str, json_key: str, json_val: bool|str|int|float) -> None:
        with open(adress) as f:
            config = json.load(f)

        config[json_key] = json_val
        with open(adress, "w") as f:
            json.dump(config, f, indent=2)


    @staticmethod
    def fix_value_in_settings(adress: str, json_key: str, default_val: bool|str|int|float) -> None:
        with open(adress) as f:
            config = json.load(f)

        if json_key not in config.keys():
            print(f"[WARNING] Key value '{json_key}' could not be found in {adress}. Resorting to default value ('{default_val}').\nFixing {adress}...")
            try:
                Utils.save_value_to_settings(adress, json_key, default_val)
                print(f"{json_key} has been fixed in {adress}")
            except Exception as e:
                print(f"{json_key} could not have been fixed in {adress}\n{e}")


    @staticmethod
    def get_val_from_settings(adress: str, json_key: str) -> str|bool:
        with open(adress) as f:
            config = json.load(f)

        temp = config[json_key]
        return temp


    @staticmethod
    def get_val_from_settings_fix(adress: str, json_key: str, default_val: str|bool) -> str|bool:
        try:
            temp = Utils.get_val_from_settings(adress, json_key)
            return temp
        except:
            Utils.fix_value_in_settings(adress, json_key, default_val)
            return default_val
