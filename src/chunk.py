import numpy as np
from typing import Literal



class Chunk():
    index_start:    int
    index_end:      int
    num_of_samples: int
    __data_array:   np.ndarray[np.float64] | np.ndarray[bool] | None
    data_mean:      np.float64 | float | None


    def __init__(
        self,
        in_start:      int,
        in_end:        int,
        in_data_array: np.ndarray[np.float64] | np.ndarray[bool] | None = None
    ) -> None:
        self.index_start    = in_start
        self.index_end      = in_end
        self.num_of_samples = in_end - in_start + 1
        self.__data_array   = in_data_array

        if in_data_array is None:
            self.data_mean = None
        else:
            self.calculate_mean_from_data()


    def calculate_mean_from_data(self) -> None:
        if self.__data_array is None:
            print("Cannot calculate chunk mean - no data present in instance")
            return

        data_sum = 0
        for element in self.__data_array:
            data_sum += element

        array_len = len(self.__data_array)
        self.data_mean = data_sum / array_len
        return


    def get_abstract_extreme(
        self,
        up_or_down: Literal["up", "down"],
        threshold:  float
    ) -> float:
        if self.__data_array is None:
            raise ValueError("[ERROR] Code is written badly. No data array in chunk!")

        temp_arr = []
        if up_or_down == "up":
            temp_arr = [val for val in self.__data_array if val > threshold]
        else:
            temp_arr = [val for val in self.__data_array if val < threshold]

        temp_extreme: float = sum(temp_arr) / len(temp_arr)
        return temp_extreme


# ================================== SETTERS ===================================
    def input_data_array(self, new_array: np.ndarray[np.float64] | np.ndarray[bool]) -> None:
        if len(new_array) != self.num_of_samples:
            raise Exception("CODE IS BROKEN. INCORRECT ARRAY LENGTH COMPARED TO INDEX VALUES!")

        self.__data_array = new_array
        return


# ================================== GETTERS ===================================
    def get_data_mean(self) -> np.float64 | float | None:
        return self.data_mean


# ================================== DELETERS ==================================
    def del_data_array(self) -> None:
        self.__data_array = None
        return
