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
        loaded_data: DataSonif = DataSonif()
        temp_success: bool     = loaded_data.get_datafile_path()
        if not temp_success:
            return
        loaded_data.load_data()

        while True:
            ordering:     str = "Original" if loaded_data.is_og_order else "Reverse"
            sign:         str = "Original" if loaded_data.is_og_sign  else "Opposite"
            segment_info: str = ("None"
                                 if loaded_data.segmentation_performed == []
                                 else str(loaded_data.segmentation_performed))

            print(f"Chosen file:           {loaded_data.file_path}")
            print(f"Data segmentation:     {segment_info}")
            print(f"Data order (x):        {ordering}")
            print(f"Data sign (y):         {sign}")
            print(f"Data normalization:    {loaded_data.is_normalized}")
            print(f"Num of bins (hist):    {loaded_data.bins_count}")
            print(f"State threshold:       {loaded_data.threshold}")
            print(f"Num of loaded samples: {loaded_data.get_sample_count()}")
            print()
            action_asker = Askers.ask_action()
            print("\n")

            # ========================== DATA ALTERING =========================
            if action_asker == "alter_data":
                while True:
                    ordering:     str = "Original" if loaded_data.is_og_order else "Reverse"
                    sign:         str = "Original" if loaded_data.is_og_sign  else "Opposite"
                    segment_info: str = ("None"
                                         if loaded_data.segmentation_performed == []
                                         else str(loaded_data.segmentation_performed))

                    print(f"Chosen file:              {loaded_data.file_path}")
                    print(f"Data segmentation:        {segment_info}")
                    print(f"Data order (x):           {ordering}")
                    print(f"Data sign (y):            {sign}")
                    print(f"Data normalization:       {loaded_data.is_normalized}")
                    print(f"Num of bins (hist/thold): {loaded_data.bins_count}")
                    print(f"State threshold:          {loaded_data.threshold}")
                    print(f"Num of loaded samples:    {loaded_data.get_sample_count()}")
                    print()
                    is_treshold = False if not loaded_data.threshold else True
                    alter_asker = Askers.ask_alter_data(
                        loaded_data.is_normalized,
                        is_treshold,
                        loaded_data.is_converted_to_binary)
                    print("\n")

                    if not alter_asker:
                        print("\n")
                        break

                    elif alter_asker   == "reverse_order":
                        print("Reversing order...")
                        loaded_data.reverse_data_order()
                        print("Done!\n\n")

                    elif alter_asker == "reverse_sign":
                        print("Reversing order...")
                        loaded_data.reverse_data_sign()
                        print("Done!\n\n")

                    elif alter_asker == "normalization":
                        print("Normalizing...")
                        loaded_data.normalize_data()
                        print("Done!\n\n")

                    elif alter_asker == "calculate_threshold":
                        print("Calculating threshold...")
                        loaded_data.calculate_threshold()
                        print("Done!\n\n")

                    elif alter_asker == "segment_data":
                        asker_segment = Askers.ask_segmentation()
                        if asker_segment is None or asker_segment == 1:
                            print("\n")
                            continue

                        print("\nSegmenting data...")
                        loaded_data.segment_data(asker_segment)
                        print("Done!\n\n")

                    elif alter_asker == "apply_paa":
                        segmenting_style = Utils.get_val_from_json_fix(
                            settings_rel_path,
                            "SEGMENTING_STYLE_PAA")

                        asker_segment_value = Askers.ask_segment_value(
                            loaded_data.get_sample_count(),
                            segmenting_style)

                        print()
                        if not asker_segment_value:
                            print()
                            continue

                        print("Processing...")
                        loaded_data.apply_paa_aggregation(
                            asker_segment_value,
                            segmenting_style)
                        print("Data successfully aggregated!\n\n")

                    elif alter_asker == "convert_to_bin":
                        print("Converting data to binary...")
                        loaded_data.convert_data_to_binary()
                        print("Done!\n\n")

                    elif alter_asker == "convert_to_dwelltimes":
                        segmenting_style = Utils.get_val_from_json_fix(
                            settings_rel_path,
                            "SEGMENTING_STYLE_DWELLTIMES")

                        asker_segment_value = Askers.ask_segment_value(
                            loaded_data.get_sample_count(),
                            segmenting_style)

                        print()
                        if not asker_segment_value:
                            print()
                            continue

                        print("Converting data to dwell times...")
                        loaded_data.convert_to_dwell_times(
                            asker_segment_value,
                            segmenting_style)
                        print("Done!\n\n")

                    elif alter_asker == "convert_to_dwelltimes_condensed":
                        segmenting_style = Utils.get_val_from_json_fix(
                            settings_rel_path,
                            "SEGMENTING_STYLE_DWELLTIMES")

                        asker_segment_value = Askers.ask_segment_value(
                            loaded_data.get_sample_count(),
                            segmenting_style)

                        print()
                        if not asker_segment_value:
                            print()
                            continue

                        print("Converting data to condensed dwell times...")
                        loaded_data.convert_to_dwell_times_CONDENSED(
                            asker_segment_value,
                            segmenting_style)
                        print("Done!\n\n")

                    elif alter_asker == "original_data":
                        if not os.path.exists(loaded_data.file_path):
                            print(f"Chosen file no longer exists in path {loaded_data.file_path}")
                            continue
                        print(loaded_data.file_path, "\n")

                        asker_segment = Askers.ask_segmentation(True)
                        if not asker_segment:
                            return
                        print("\n")

                        loaded_data = DataSonif(loaded_data.file_path, asker_segment)


            # ========================== OTHER OPTIONS =========================
            elif action_asker == "sonify":
                asker_sonif_type = Askers.ask_sonif_type(
                    loaded_data.is_converted_to_binary,
                    loaded_data.is_normalized)
                print("\n\n")

                if not asker_sonif_type:
                    continue
                elif asker_sonif_type == "binary":
                    loaded_data.binary_sonif_loop(settings_rel_path, notes_rel_path)
                    print("\n\n")
                elif asker_sonif_type == "analog":
                    loaded_data.analog_sonif_loop(settings_rel_path, notes_rel_path)
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

            elif action_asker == "change_file":
                break

            elif action_asker == "exit":
                return

            else:
                print("Invallid input.\n\n")
