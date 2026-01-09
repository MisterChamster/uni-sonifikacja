from pathlib import Path
import os
from src.askers import Askers
from src.datasonif import DataSonif
from src.utils import Utils
from src.settings_loop import settings_loop



def mainloop() -> None:
    settings_rel_path = "src/settings.json"
    notes_rel_path = "src/notes.json"
    while True:
        print("Choose data file in txt/csv format:")
        datafile_path = Askers.ask_path_filedialog("f", "Choose data txt file")
        if not datafile_path:
            print("No file has been chosen.")
            return
        if not datafile_path.endswith((".txt", ".csv")):
            print("Wrong file format.")
            return
        print(datafile_path, "\n")

        asker_segment = Askers.ask_segmentation(True)
        if not asker_segment:
            return
        print("\n")

        datafile_path = Path(datafile_path)
        loaded_data   = DataSonif(datafile_path, asker_segment)

        while True:
            segment_info = "False" if asker_segment == 1  else str(asker_segment)
            ordering = "Original" if loaded_data.og_order else "Reverse"
            sign     = "Original" if loaded_data.og_sign  else "Opposite"

            print(f"Chosen file:        {loaded_data.file_path}")
            print(f"Data segmentation:  {segment_info}")
            print(f"Data order (x):     {ordering}")
            print(f"Data sign (y):      {sign}")
            print(f"Data normalization: {loaded_data.normalized}")
            print(f"Num of bins (hist): {loaded_data.bins_count}")
            print(f"State threshold:    {loaded_data.threshold}\n")
            action_asker = Askers.ask_action()
            print()

            if action_asker   == "reverse_order":
                print("Reversing order...")
                loaded_data.reverse_data_order()
                print("Done!\n\n")

            elif action_asker == "reverse_sign":
                print("Reversing order...")
                loaded_data.reverse_data_sign()
                print("Done!\n\n")

            elif action_asker == "normalization":
                print("Normalizing...")
                loaded_data.normalize_data()
                print("Done!\n\n")

            elif action_asker == "calculate_threshold":
                print("Calculating threshold...")
                loaded_data.calculate_threshold()
                print("Done!\n\n")

            elif action_asker == "apply_paa":
                segmenting_style = Utils.get_val_from_json_fix(
                    settings_rel_path,
                    "SEGMENTING_STYLE_PAA",
                    "count"
                )

                asker_segment_value = Askers.ask_segment_value(
                    loaded_data.get_sample_count(),
                    segmenting_style
                )
                if asker_segment_value is None:
                    print()
                    continue
                print()

                print("Processing...")
                loaded_data.apply_paa_aggregation(
                    asker_segment_value,
                    segmenting_style)
                print("Data successfully aggregated!\n\n")

            elif action_asker == "convert_to_bin":
                print("Converting data to binary...")
                loaded_data.convert_data_to_binary()
                print("Done!\n\n")

            elif action_asker == "convert_to_dwelltimes":
                segmenting_style = Utils.get_val_from_json_fix(
                    settings_rel_path,
                    "SEGMENTING_STYLE_DWELLTIMES",
                    "size"
                )

                asker_segment_value = Askers.ask_segment_value(
                    loaded_data.get_sample_count(),
                    segmenting_style
                )
                if asker_segment_value is None:
                    print()
                    continue
                print()

                print("Converting data to dwell times...")
                loaded_data.convert_to_dwell_times(
                    asker_segment_value,
                    segmenting_style
                )
                print("Done!\n\n")

            elif action_asker == "sonify":
                asker_sonif_type = Askers.ask_sonif_type(
                    loaded_data.converted_to_binary,
                    #COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE
                    # COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE COME_BACK_HER
                    #COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE
                    # COME_BACK_HERE COME_BACK_HERE COME_BACK_HERE COME_BACK_HER
                    False)
                print("\n\n")

                if not asker_sonif_type:
                    continue
                elif asker_sonif_type == "binary":
                    loaded_data.binary_sonif_loop(settings_rel_path, notes_rel_path)
                    print("\n\n")
                elif asker_sonif_type == "analog":
                    # CONTINUE WRITING HERE
                    # self.analog_sonif_loop(settings_rel_adress, notes_rel_adress)
                    print("\n\n")

            elif action_asker == "show_chart":
                print("Preparing chart...\n")
                loaded_data.show_chart()
                print()

            elif action_asker == "show_histogram":
                print("Preparing histogram...\n")
                loaded_data.show_histogram()
                print()

            elif action_asker == "settings":
                settings_loop(settings_rel_path, notes_rel_path)
                print("\n")

            elif action_asker == "original_data":
                if not os.path.exists(datafile_path):
                    print(f"Chosen file no longer exists in path {datafile_path}")
                    continue
                print(datafile_path, "\n")

                asker_segment = Askers.ask_initial_segmentation()
                if not asker_segment:
                    return
                print("\n")

                loaded_data = DataSonif(datafile_path, asker_segment)

            elif action_asker == "change_file":
                break

            elif action_asker == "exit":
                return
