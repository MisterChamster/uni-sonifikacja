from src.askers import Askers
from src.utils  import Utils



def settings_loop(settings_rel_adress: str) -> None:
    while True:
        asker_settings: str = Askers.ask_settings()

        if not asker_settings:
            return

        if asker_settings == "auto_threshold_at_load":
            Utils.change_setting_to_opposite("AUTOMATIC_THRESHOLD_AT_LOAD")
            print("Value successfully changed\n")

        elif asker_settings == "show_thold_chart":
            Utils.change_setting_to_opposite("SHOW_THRESHOLD_ON_CHARTS")
            print("Value successfully changed\n")

        elif asker_settings == "change_cutting_setting_paa":
            Utils.change_setting_to_opposite("CUT_REMAINDER_SAMPLES_PAA")
            print("Value successfully changed\n")

        elif asker_settings == "change_cutting_setting_dwelltimes":
            Utils.change_setting_to_opposite("CUT_REMAINDER_SAMPLES_DWELLTIMES")
            print("Value successfully changed\n")

        elif asker_settings == "change_segmenting_setting_paa":
            Utils.change_setting_to_opposite("SEGMENTING_STYLE_PAA")
            print("Value successfully changed\n")

        elif asker_settings == "change_segmenting_setting_dwelltimes":
            Utils.change_setting_to_opposite("SEGMENTING_STYLE_DWELLTIMES")
            print("Value successfully changed\n")

        elif asker_settings == "change_binary_low_note":
            new_note = Askers.ask_note_binary("low")
            if not new_note:
                continue
            Utils.save_value_to_settings(
                settings_rel_adress,
                "BINARY_SONIFICATION_LOW_NOTE",
                new_note)
            print("Value successfully changed\n")

        elif asker_settings == "change_binary_high_note":
            new_note = Askers.ask_note_binary("high")
            if not new_note:
                continue
            Utils.save_value_to_settings(
                settings_rel_adress,
                "BINARY_SONIFICATION_HIGH_NOTE",
                new_note)
            print("Value successfully changed\n")

        else:
            print("Invalid input!\n")
