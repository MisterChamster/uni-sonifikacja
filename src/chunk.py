import numpy as np



class Chunk():
    index_start:    int
    index_end:      int
    num_of_samples: int
    data_mean:      np.float64 | None
    __data_array:   np.ndarray[np.float64] | None

    def __init__(
        self,
        in_start:      int,
        in_end:        int,
        in_data_array: np.ndarray[np.float64] | None = None
    ) -> None:
        self.index_start    = in_start
        self.index_end      = in_end
        self.num_of_samples = in_end - in_start + 1
        self.__data_array   = in_data_array

        if not in_data_array:
            self.data_mean = None
        else:
            self.calculate_mean_from_data()


    def calculate_mean_from_data(self) -> None:
        if not self.__data_array:
            print("Cannot calculate chunk mean - no data present in instance")
            return

        data_sum = 0
        for element in self.__data_array:
            data_sum += element

        array_len = len(self.__data_array)
        self.data_mean = data_sum / array_len
        return


    def input_data_array(self, new_array: np.ndarray[np.float64]) -> None:
        if len(new_array) != self.num_of_samples:
            raise Exception("CODE IS BROKEN. INCORRECT ARRAY LENGTH COMPARED TO INDEX VALUES!")

        self.__data_array = new_array
        return


    def get_data_mean(self) -> np.float64 | None:
        return self.data_mean
