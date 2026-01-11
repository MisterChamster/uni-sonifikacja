import numpy as np



class Chunk():
    index_start: int
    index_end:   int
    data_mean:   float | None
    data_array:  np.ndarray | None

    def __init__(self, in_start: int, in_end: int):
        self.index_start = in_start
        self.index_end   = in_end
        self.data_mean   = None
        self.data_array  = None
