from pathlib import Path
from typing  import Literal
import os

from src.askers        import Askers
from src.datasonif     import DataSonif
from src.utils         import Utils
from src.settings_loop import settings_loop
from src.note          import Note



src_path = Path(__file__).resolve().parent
filebox_startpath = str(src_path.parent / "data")
settings_path: Path = src_path / "settings.json"
notes_path:    Path = src_path / "settings.json"
Askers.settings_path    = settings_path
Askers.notes_path       = notes_path
Utils.settings_path     = settings_path
Utils.notes_path        = notes_path
DataSonif.settings_path = settings_path
DataSonif.notes_path    = notes_path

sample_rate: int = Utils.get_val_from_settings_fix("SAMPLE_RATE")
DataSonif.sample_rate = sample_rate
Note.sample_rate      = sample_rate

sonif_sim_thold: int = Utils.get_val_from_settings_fix("SONIF_SIMILARITY_THRESHOLD")
Note.similatiry_threshold = sonif_sim_thold


def mainloop() -> None:
    """
    Open main menu and handle user input.

    This is a program's strating point and main menu. It begins with 
    prompting user to choose a txt/csv file to load data from. Then, main 
    menu begins where user is presented with various options to choose from. 
    Their options are:
    - Process data, which opens a menu asking them for specific processing 
    technique and responding accordingly.
    - Sonify data, which opens a menu to choose correct sonificatin type 
    and handling responses accordingy.
    - Show chart, which charts loaded data.
    - Show histogram, which prints data values on a histogram with 200 bins.
    - Settings, which opens settings loop.
    - Load original data, which loads data again from the same file.
    - Change file, which loads data from a different file chosen by user.
    - Exit, which exits the program.
    """

    while True:
        loaded_data: DataSonif = DataSonif()
        temp_success:     bool = loaded_data.get_datafile_path(filebox_startpath)
        if not temp_success:
            return
        load_success: bool = loaded_data.load_data()
        if not load_success:
            print("Data has not been loaded.\n\n")
            continue

        while True:
            downsampling_info: str = (
                "None"
                if loaded_data.downsampling_performed == []
                else " ,".join(map(str, loaded_data.downsampling_performed)))

            print(f"Chosen file:           {loaded_data.file_path}")
            print(f"Data downsampling:     {downsampling_info}")
            print(f"Data normalization:    {loaded_data.is_normalized}")
            print(f"Num of bins (hist):    {loaded_data.bins_count}")
            print(f"State threshold:       {loaded_data.threshold:.4f}")
            print(f"Num of loaded samples: {loaded_data.get_sample_count()}")
            print()
            action_asker = Askers.ask_action()
            print("\n")

            # ========================= DATA PROCESSING ========================
            if action_asker == "process_data":
                while True:
                    downsampling_info: str = (
                        "None"
                        if loaded_data.downsampling_performed == []
                        else " ,".join(map(str, loaded_data.downsampling_performed)))

                    print(f"Chosen file:              {loaded_data.file_path}")
                    print(f"Data downsampling:        {downsampling_info}")
                    print(f"Data normalization:       {loaded_data.is_normalized}")
                    print(f"Num of bins (hist/thold): {loaded_data.bins_count}")
                    print(f"State threshold:          {loaded_data.threshold:.4f}")
                    print(f"Num of loaded samples:    {loaded_data.get_sample_count()}")
                    print()
                    is_treshold = False if not loaded_data.threshold else True
                    data_processing_asker = Askers.ask_process_data(
                        loaded_data.is_normalized,
                        is_treshold,
                        loaded_data.is_converted_to_binary)
                    print("\n")

                    if not data_processing_asker:
                        break

                    elif data_processing_asker == "reverse_order":
                        print("Reversing order...")
                        loaded_data.reverse_data_order()
                        print("Done!\n\n")

                    elif data_processing_asker == "reverse_sign":
                        print("Reversing order...")
                        loaded_data.reverse_data_sign()
                        print("Done!\n\n")

                    elif data_processing_asker == "normalization":
                        print("Normalizing...")
                        loaded_data.normalize_data()
                        print("Done!\n\n")

                    elif data_processing_asker == "calculate_threshold":
                        print("Calculating threshold...")
                        loaded_data.calculate_threshold()
                        print("Done!\n\n")

                    elif data_processing_asker == "downsample_data":
                        asker_downsample = Askers.ask_downsampling()
                        if not asker_downsample or asker_downsample == 1:
                            print("\n")
                            continue

                        print("\nDownsampling data...")
                        loaded_data.downsample_data(asker_downsample)
                        print("Done!\n\n")

                    elif data_processing_asker == "apply_paa":
                        segmenting_style_paa: Literal["count", "size"] = Utils.get_val_from_settings_fix(
                            "SEGMENTING_STYLE_PAA")

                        asker_segment_value = Askers.ask_segment_value(
                            loaded_data.get_sample_count(),
                            segmenting_style_paa)

                        print()
                        if not asker_segment_value:
                            print()
                            continue

                        print("Processing...")
                        loaded_data.apply_paa_aggregation(
                            asker_segment_value,
                            segmenting_style_paa)
                        print("Data successfully aggregated!\n\n")

                    elif data_processing_asker == "convert_to_bin":
                        print("Converting data to binary...")
                        loaded_data.convert_data_to_binary()
                        print("Done!\n\n")

                    elif data_processing_asker == "convert_to_dwelltimes":
                        segmenting_style_dwt: Literal["count", "size"] = Utils.get_val_from_settings_fix(
                            "SEGMENTING_STYLE_DWELLTIMES")

                        asker_segment_value = Askers.ask_segment_value(
                            loaded_data.get_sample_count(),
                            segmenting_style_dwt)

                        print()
                        if not asker_segment_value:
                            print()
                            continue

                        print("Converting data to dwell times...")
                        loaded_data.convert_to_dwell_times(
                            asker_segment_value,
                            segmenting_style_dwt)
                        print("Done!\n\n")

                    elif data_processing_asker == "convert_to_dwelltimes_reduced":
                        segmenting_style_dwt: Literal["count", "size"] = Utils.get_val_from_settings_fix(
                            "SEGMENTING_STYLE_DWELLTIMES")

                        asker_segment_value = Askers.ask_segment_value(
                            loaded_data.get_sample_count(),
                            segmenting_style_dwt)

                        print()
                        if not asker_segment_value:
                            print()
                            continue

                        print("Converting data to reduced dwell times...")
                        loaded_data.convert_to_dwell_times_REDUCED(
                            asker_segment_value,
                            segmenting_style_dwt)
                        print("Done!\n\n")

                    elif data_processing_asker == "appy_emd":
                        print("Applying EMD...")
                        emd_applied = loaded_data.apply_emd()
                        if emd_applied:
                            print("Done!\n\n")


            # ========================== OTHER OPTIONS =========================
            elif action_asker == "sonify":
                asker_sonif_type = Askers.ask_sonif_type(
                    loaded_data.is_converted_to_binary,
                    loaded_data.is_normalized)
                print("\n\n")

                if not asker_sonif_type:
                    continue
                elif asker_sonif_type == "binary":
                    loaded_data.binary_sonif_loop()
                    print("\n\n")
                elif asker_sonif_type == "analog":
                    loaded_data.analog_sonif_loop()
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
                settings_loop()
                print("\n")

            elif action_asker == "original_data":
                if not os.path.exists(loaded_data.file_path):
                    print(f"Chosen file no longer exists in path {loaded_data.file_path}")
                    continue
                print(loaded_data.file_path, "\n")
                load_success: bool = loaded_data.load_data()
                if not load_success:
                    print("Data has not been loaded.\n\n")
                continue

            elif action_asker == "change_file":
                loaded_data: DataSonif = DataSonif()
                temp_success: bool     = loaded_data.get_datafile_path(filebox_startpath)
                if not temp_success:
                    print("Data will remain unchanged\n\n")
                    continue
                load_success: bool = loaded_data.load_data()
                if not load_success:
                    print("Data has not been loaded.\n\n")

            elif action_asker == "exit":
                return

            else:
                print("Invallid input.\n\n")
