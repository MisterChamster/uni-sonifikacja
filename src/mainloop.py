from src.askers import ask_path_filedialog, ask_normalize
from src.utils import get_open_close_for_chunks, get_peak_coordinates
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
# So, a border reasonable num of putting rows in chart with loaded_boi.hist()
# is around 25k which is 15 seconds. More than that will be a slog and we
# don't want that.



def mainloop() -> None:
    asker_normalize = ask_normalize()
    print()

    print("Choose data file in txt/csv format:")
    datafile_path = ask_path_filedialog("f", "Choose data txt file")
    if not datafile_path.endswith(".txt") and not datafile_path.endswith(".csv"):
        print("Wrong file format")
        return
    print(datafile_path)

    # Load file
    print("Loading file...\n")
    segmenter = 5   #To get every 5th line
    loaded_boi = pd.read_csv(datafile_path,
                             header=None,
                             names=["values"],
                             skiprows=lambda i: i % segmenter != 0,
                             skipinitialspace=True)

    # Get pandas.Series objects and convert them to floats. There was a
    # FutureWarning regarding a blatant type casting to float :((
    min_ds_val = loaded_boi.min()
    min_ds_val = float(min_ds_val["values"])
    max_ds_val = loaded_boi.max()
    max_ds_val = float(max_ds_val["values"])
    diff = max_ds_val-min_ds_val

    # Getting peaks
    # general_chunk_vals = get_open_close_for_chunks(datafile_path, 2000, min_ds_val, max_ds_val)
    print("Getting peak coords...\n")
    peak_coords = get_peak_coordinates(datafile_path, 2000, min_ds_val, max_ds_val)
    peak_xes = [a[0] for a in peak_coords]
    peak_ys  = [a[1] for a in peak_coords]

    # Normalization xnorm = (x-xmin)\(xmax-xmin)
    if asker_normalize == True:
        print("Normalizing...\n")
        loaded_boi = loaded_boi.map(lambda x: (x-min_ds_val)/(diff))
        print(loaded_boi)

        for i in range(len(peak_ys)):
            peak_ys[i] = (peak_ys[i]-min_ds_val)/(diff)

    print("Plotting (evil plans)...\n")
    plt.scatter(loaded_boi.index, loaded_boi["values"], s=1)
    plt.scatter(peak_xes, peak_ys, marker="x", colorizer="red", s=220, linewidths=3)

    plt.xlabel("Samples")
    plt.ylabel("Value")
    if asker_normalize == True:
        y_locators = 0.1
    else:
        y_locators = 1
    plt.gca().xaxis.set_major_locator(MultipleLocator(10000))
    plt.gca().yaxis.set_major_locator(MultipleLocator(y_locators))
    plt.title('A VERY Cool Chart')
    plt.show()
