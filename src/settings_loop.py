from src.askers import Askers
from src.utils import Utils



def settings_loop(
    settings_rel_adress: str,
    notes_rel_adress: str
) -> None:
    while True:
        asker_settings: str = Askers.ask_settings(settings_rel_adress)

        if asker_settings == "change_cutting_setting_paa":
            Utils.change_setting_to_opposite(
                settings_rel_adress,
                "CUT_REMAINDER_SAMPLES_PAA",
                True)
            print("Value successfully changed\n")

        elif asker_settings == "change_cutting_setting_dwelltimes":
            Utils.change_setting_to_opposite(
                settings_rel_adress,
                "CUT_REMAINDER_SAMPLES_DWELLTIMES",
                True)
            print("Value successfully changed\n")

        elif asker_settings == "change_segmenting_setting_paa":
            Utils.change_setting_to_opposite(
                settings_rel_adress,
                "SEGMENTING_STYLE_PAA",
                "size")
            print("Value successfully changed\n")

        elif asker_settings == "change_segmenting_setting_dwelltimes":
            Utils.change_setting_to_opposite(
                settings_rel_adress,
                "SEGMENTING_STYLE_DWELLTIMES",
                "size")
            print("Value successfully changed\n")

        elif asker_settings == "change_binary_low_note":
            new_note = Askers.ask_note_binary(notes_rel_adress, "low")
            if not new_note:
                continue
            Utils.save_value_to_settings(
                settings_rel_adress,
                "BINARY_SONIFICATION_LOW_NOTE",
                new_note)
            print("Value successfully changed\n")

        elif asker_settings == "change_binary_high_note":
            new_note = Askers.ask_note_binary(notes_rel_adress, "high")
            if not new_note:
                continue
            Utils.save_value_to_settings(
                settings_rel_adress,
                "BINARY_SONIFICATION_HIGH_NOTE",
                new_note)
            print("Value successfully changed\n")

        elif asker_settings == "exit":
            return

        else:
            print("Invalid input!\n")
