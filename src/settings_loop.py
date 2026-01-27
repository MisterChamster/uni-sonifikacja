from src.askers import Askers
from src.utils  import Utils



def settings_loop() -> None:
    """
    Open settings menu and handle user input.

    Opens a menu to choose settings type. Then, depending on the answer 
    returns to main menu, opens processing settings or sonification settings. 
    After that it opens a menu for specific settings type and allows 
    user to pick the value they want to change. When values are on/off 
    toggle style, picking them just changes their state. When values are 
    non-boolean, user is prompted to input a value or return. User stays 
    in function loop as long as they want to until inputing 'r' to return 
    to main loop.
    """

    msg_val_changed = "Value successfully changed\n\n"

    settings_type = Askers.ask_settings_type()
    if not settings_type:
        return

    print("\n")
    if settings_type == "data_settings":
        while True:
            asker_settings: str|None = Askers.ask_data_settings()

            if not asker_settings:
                return

            if asker_settings == "auto_normalization_at_load":
                Utils.change_setting_to_opposite("AUTOMATIC_NORMALIZATION_AT_LOAD")
                print(msg_val_changed)

            elif asker_settings == "auto_threshold_at_load":
                Utils.change_setting_to_opposite("AUTOMATIC_THRESHOLD_AT_LOAD")
                print(msg_val_changed)

            elif asker_settings == "show_thold_chart":
                Utils.change_setting_to_opposite("SHOW_THRESHOLD_ON_CHARTS")
                print(msg_val_changed)

            elif asker_settings == "change_cutting_setting_paa":
                Utils.change_setting_to_opposite("CUT_REMAINDER_SAMPLES_PAA")
                print(msg_val_changed)

            elif asker_settings == "change_cutting_setting_dwelltimes":
                Utils.change_setting_to_opposite("CUT_REMAINDER_SAMPLES_DWELLTIMES")
                print(msg_val_changed)

            elif asker_settings == "change_segmenting_setting_paa":
                Utils.change_setting_to_opposite("SEGMENTING_STYLE_PAA")
                print(msg_val_changed)

            elif asker_settings == "change_segmenting_setting_dwelltimes":
                Utils.change_setting_to_opposite("SEGMENTING_STYLE_DWELLTIMES")
                print(msg_val_changed)

            elif asker_settings == "change_imfs_from":
                print()
                asker = Askers.ask_new_imfs_from()
                if not asker:
                    print("\n")
                    continue
                Utils.save_value_to_settings(
                    "EMD_CONSIDER_IMFS_FROM",
                    asker)
                print(msg_val_changed)

            else:
                print("Invalid input!\n")

    elif settings_type == "sonif_settings":
        while True:
            asker_settings: str|None = Askers.ask_sonif_settings()

            if not asker_settings:
                return

            elif asker_settings == "change_binary_low_note":
                print()
                new_note = Askers.ask_note_binary("low")
                if not new_note:
                    print("\n")
                    continue
                Utils.save_value_to_settings(
                    "BINARY_SONIF_LOW_NOTE",
                    new_note)
                print(msg_val_changed)

            elif asker_settings == "change_binary_high_note":
                print()
                new_note = Askers.ask_note_binary("high")
                if not new_note:
                    print("\n")
                    continue
                Utils.save_value_to_settings(
                    "BINARY_SONIF_HIGH_NOTE",
                    new_note)
                print(msg_val_changed)

            elif asker_settings == "change_similarity_threshold":
                print()
                new_sim_thold = Askers.ask_similarity_threshold()
                if not new_sim_thold:
                    print("\n")
                    continue
                Utils.save_value_to_settings(
                    "SONIF_SIMILARITY_THRESHOLD",
                    new_sim_thold)
                print(msg_val_changed)

            else:
                print("Invalid input!\n")
