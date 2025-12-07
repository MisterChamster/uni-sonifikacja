from src.Askers import Askers
from src.DataSonif import DataSonif



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
    print()

    loaded_data = DataSonif(datafile_path, asker_segment)

    while True:
        action_asker = Askers.ask_action()
        print()
        if action_asker == "normalization":
            print("Normalizing...")
            loaded_data.normalize_data()
            print("Done!\n\n")

        elif action_asker == "calculate_threshold":
            print("This functionality is yet to be developed...\n")

        elif action_asker == "show_chart":
            print("Preparing chart...\n")
            loaded_data.show_chart()

        elif action_asker == "show_histogram":
            print("This functionality is yet to be developed...\n")

        elif action_asker == "exit":
            break

        # asker_normalize = Askers.ask_normalize()
        # print()

        # min_ds_val = loaded_data.min()
        # min_ds_val = float(min_ds_val["values"])
        # max_ds_val = loaded_data.max()
        # max_ds_val = float(max_ds_val["values"])
        # diff = max_ds_val-min_ds_val

        # general_chunk_vals = get_open_close_for_chunks(datafile_path, 2000, min_ds_val, max_ds_val)
        # peak_coords = get_peak_coordinates(datafile_path, 2000, min_ds_val, max_ds_val)
        # peak_xes = [a[0] for a in peak_coords]
        # peak_ys  = [a[1] for a in peak_coords]

        # if asker_normalize == True:
            # loaded_data = loaded_data.map(lambda x: (x-min_ds_val)/(diff))
            # print(loaded_data)

            # for i in range(len(peak_ys)):
            #     peak_ys[i] = (peak_ys[i]-min_ds_val)/(diff)

        # plt.scatter(loaded_data.index, loaded_data["values"], s=1)
        # plt.scatter(peak_xes, peak_ys, marker="x", colorizer="red", s=220, linewidths=3)

        # if asker_normalize == True:
        #     y_locators = 0.1
        # else:
        #     y_locators = 1
        # plt.gca().xaxis.set_major_locator(MultipleLocator(10000))
        # plt.gca().yaxis.set_major_locator(MultipleLocator(y_locators))
        # plt.show()
