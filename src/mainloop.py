from src.askers import Askers
from src.datasonif import DataSonif



def mainloop() -> None:
    print("Choose data file in txt/csv format:")
    datafile_path = Askers.ask_path_filedialog("f", "Choose data txt file")
    if not datafile_path.endswith((".txt", ".csv")):
        print("Wrong file format")
        return
    print(datafile_path, "\n")

    # Load file
    print("Loading file...\n")
    asker_segment = Askers.ask_segment()
    print("\n")

    loaded_data = DataSonif(datafile_path, asker_segment)

    while True:
        print(f"Chosen file:        {loaded_data.file_path}")
        print(f"Data segmentation:  {asker_segment}")
        print(f"Data normalization: {loaded_data.normalized}")
        print(f"State treshold:     {loaded_data.treshold}\n")
        action_asker = Askers.ask_action()
        print()
        if action_asker == "normalization":
            print("Normalizing...")
            loaded_data.normalize_data()
            print("Done!\n\n")

        elif action_asker == "calculate_threshold":
            print("This functionality is yet to be developed...\n\n")

        elif action_asker == "show_chart":
            print("Preparing chart...\n")
            loaded_data.show_chart()
            print()

        elif action_asker == "show_histogram":
            print("This functionality is yet to be developed...\n\n")

        elif action_asker == "exit":
            break
