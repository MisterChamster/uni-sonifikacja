import numpy as np



class Chunk():
    index_start:    int
    index_end:      int
    num_of_samples: int
    data_mean:      float | None
    __data_array:   np.ndarray[np.float64] | None

    def __init__(self, in_start: int, in_end: int):
        self.index_start    = in_start
        self.index_end      = in_end
        self.num_of_samples = in_end - in_start + 1
        self.data_mean      = None
        self.__data_array   = None

    def calculate_mean_from_data(self) -> None:
        if not self.__data_array:
            print("Cannot calculate chunk mean - no data present in instance")
            return

        data_sum = 0
        for element in self.__data_array:
            data_sum += element

        array_len = len(self.__data_array)
        self.mean = data_sum / array_len
        return


    def input_data_array(self, new_array: np.ndarray[np.float64]) -> None:
        if len(new_array) != self.num_of_samples:
            raise Exception("CODE IS BROKEN. INCORRECT ARRAY LENGTH COMPARED TO INDEX VALUES!")

        self.__data_array = new_array
        return
