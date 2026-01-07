from src.askers import Askers
from src.utils import Utils



def settings_loop() -> None:
    while True:
        asker_settings: str = Askers.ask_settings()

        if asker_settings == "change_cutting_setting_paa":
            Utils.change_setting_to_opposite(
                "src/settings.json",
                "CUT_REMAINDER_STRING_PAA",
                True)
            print()
        elif asker_settings == "change_cutting_setting_dwelltimes":
            Utils.change_setting_to_opposite(
                "src/settings.json",
                "CUT_REMAINDER_STRING_DWELLTIMES",
                True)
        elif asker_settings == "change_segmenting_setting_paa":
            Utils.change_setting_to_opposite(
                "src/settings.json",
                "SEGMENTING_PAA",
                "size")
        elif asker_settings == "change_segmenting_setting_dwelltimes":
            Utils.change_setting_to_opposite(
                "src/settings.json",
                "SEGMENTING_DWELLTIMES",
                "size")
        elif asker_settings == "exit":
            return

        print("Value successfully changed\n")
