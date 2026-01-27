import numpy as np



class Chunk():
    """
    Representation of a data segment.

    This is a helper class that assists with segmentation of data. It is 
    capable of calculating data mean. Serves to make program more abstract 
    and easier to understand.

    Attributes:
        index_start (int): Index in the main array where data from Chunk instance begins.
        index_end (int): Index in the main array where data from Chunk instance ends.
        num_of_samples (int): Number of samples present in Chunk.
        __data_array (np.ndarray[np.float64] | np.ndarray[bool] | None): Data present in Chunk.
        data_mean (np.float64 | float | None): Mean of all samples present in Chunk.
    """
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
        """
        Initialize Chunk instance.

        Initializes Chunk instance. Calculates number of samples. Calculates 
        samples mean if possible.

        Args:
            in_start: Index in the main array where data from Chunk instance begins.
            in_end: Index in the main array where data from Chunk instance ends.
            in_data_array: Data present in Chunk.
        """
        self.index_start    = in_start
        self.index_end      = in_end
        self.num_of_samples = in_end - in_start + 1
        self.__data_array   = in_data_array

        if in_data_array is None:
            self.data_mean = None
        else:
            self.calculate_mean_from_data()


    def calculate_mean_from_data(self) -> None:
        """

        """
        if self.__data_array is None:
            print("Cannot calculate chunk mean - no data present in instance")
            return

        data_sum = 0
        for element in self.__data_array:
            data_sum += element

        array_len = len(self.__data_array)
        self.data_mean = data_sum / array_len
        return


# ================================== SETTERS ===================================
    def input_data_array(self, new_array: np.ndarray[np.float64] | np.ndarray[bool]) -> None:
        """
        Set new data array

        Args:
            new_array: An array to become new __data_array field.
        """
        if len(new_array) != self.num_of_samples:
            raise Exception("CODE IS BROKEN. INCORRECT ARRAY LENGTH COMPARED TO INDEX VALUES!")

        self.__data_array = new_array.copy()
        self.calculate_mean_from_data()
        return


# ================================== GETTERS ===================================
    def get_data_mean(self) -> np.float64:
        """
        Get data mean.

        Returns:
            Mean of loaded data.

        Raises:
            Error: If these's no mean calculated.
        """
        if self.data_mean is None:
            raise Exception("CODE IS BROKEN. NO DATA MEAN HAS BEEN CALCULATED!")
        return self.data_mean


# ================================== DELETERS ==================================
    def del_data_array(self) -> None:
        """
        Free up __data_array field space.
        """
        self.__data_array = None
        return
