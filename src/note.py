import numpy as np
from src.utils import Utils



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
        # Utils.draw_tone(self.tone)
        # for i in range(30):
        #     print("HELLO", str(i) + ".", self.tone[i])
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

    def is_freq_rising_start(self) -> bool:
        if self.tone[0] < self.tone[1]:
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


    def cut_tone_to_match(
        self,
        is_freq_rising: bool,
        last_freq: float,
        longest_wavelen_in_samples: int
    ) -> None:
        for _ in range(longest_wavelen_in_samples):
            if not is_freq_rising and self.is_freq_rising_start():
                continue
            if is_freq_rising and not self.is_freq_rising_start():
                continue
            # If not are similar
            # COME BACK HERE
            # My approximation threshold will be 0.05. This value can be changed,
            # but I think that it'll make little, if any, noticeable difference.
            # That value probably can be safely lowered l8r!
        return
