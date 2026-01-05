from src.askers import Askers
from src.datasonif import DataSonif
from pathlib import Path
import json
from src.utils import Utils



def mainloop() -> None:
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

        asker_segment = Askers.ask_initial_segmentation()
        if not asker_segment:
            return
        print("\n")

        datafile_path = Path(datafile_path)
        loaded_data = DataSonif(datafile_path, asker_segment)

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
            print(f"State treshold:     {loaded_data.treshold}\n")
            action_asker = Askers.ask_action()
            print()

            if action_asker == "reverse_order":
                print("Reversing order...")
                loaded_data.reverse_data_order()
                print("Done!\n\n")

            elif action_asker == "reverse_sign":
                print("Reversing order...")
                loaded_data.reverse_data_sign()
                print("Done!\n\n")

            elif action_asker == "apply_paa":
                asker_segment_paa = Askers.ask_segment_count_paa(loaded_data.get_sample_count())
                print()
                if asker_segment_paa is None:
                    print()
                    continue

                print("Processing...")
                loaded_data.apply_paa_aggregation(asker_segment_paa)
                print("Data successfully aggregated!\n\n")

            elif action_asker == "normalization":
                print("Normalizing...")
                loaded_data.normalize_data()
                print("Done!\n\n")

            elif action_asker == "calculate_threshold":
                print("Calculating treshold...")
                loaded_data.calculate_treshold()
                print("Done!\n\n")

            elif action_asker == "convert_to_bin":
                print("Converting data to binary...")
                loaded_data.convert_data_to_binary()
                print("Done!\n\n")

            elif action_asker == "convert_to_dwelltimes":
                print("Converting data to dwell times...")
                loaded_data.convert_to_dwell_times()
                print("Done!\n\n")

            elif action_asker == "show_chart":
                print("Preparing chart...\n")
                loaded_data.show_chart()
                print()

            elif action_asker == "show_histogram":
                print("Preparing histogram...\n")
                loaded_data.show_histogram()
                print()

            elif action_asker == "settings":
                asker_settings: str = Askers.ask_settings()

                if asker_settings == "change_cutting_setting_paa":
                    Utils.change_setting_to_opposite("src/settings.json",
                                                     "CUT_REMAINDER_STRING_PAA",
                                                     True)
                elif asker_settings == "change_cutting_setting_dwelltimes":
                    Utils.change_setting_to_opposite("src/settings.json",
                                                     "CUT_REMAINDER_STRING_DWELLTIMES",
                                                     True)
                elif asker_settings == "change_segmenting_setting_paa":
                    Utils.change_setting_to_opposite("src/settings.json",
                                                     "SEGMENTING_PAA",
                                                     "size")
                elif asker_settings == "change_segmenting_setting_dwelltimes":
                    Utils.change_setting_to_opposite("src/settings.json",
                                                     "SEGMENTING_DWELLTIMES",
                                                     "size")
                print("\n")

            elif action_asker == "change_file":
                break

            elif action_asker == "exit":
                return
