import numpy as np



class Note():
    sample_rate: int
    freq: float
    length_ms: int
    length_sec: float
    linspace: np.ndarray#[np.float64]
    tone: np.ndarray#IDK
    lowest_note_wavelen_samples_roundup: int
    last_freq: float

    #Not finished
    def __init__(
        self,
        in_s_rate: int,
        in_freq: float,
        in_len_ms: int,
        in_longest_wavelen_samples: int
    ) -> None:
        self.sample_rate = in_s_rate
        self.freq = in_freq
        self.length_ms = in_len_ms
        self.length_sec = in_len_ms / 1000
        self.lowest_note_wavelen_samples_roundup = in_longest_wavelen_samples

        self.linspace = np.linspace(0,
            self.length_sec,
            int(self.sample_rate * self.length_sec),
            endpoint=False)
        return


    #UNSAFE
    def calculate_tone(self) -> None:
        self.tone = np.sin(2 * np.pi * self.freq * self.linspace)
        self.last_freq = self.tone[-1]
        return


    def get_tone(self) -> np.ndarray:
        return self.tone


    def get_last_freq(self) -> float:
        return self.last_freq


    # Unsafe!
    def is_freq_rising_end(self) -> bool:
        if self.tone[-2] < self.tone[-1]:
            return True
        return False
    

    def extend_linspace_with_lowest_note(self) -> None:
        lowest_wavelen_sec: float = self.sample_rate / self.lowest_note_wavelen_samples_roundup
        new_length = lowest_wavelen_sec + self.length_sec

        self.linspace = np.linspace(0,
            self.length_sec,
            int(self.sample_rate * new_length),
            endpoint=False)
        return
