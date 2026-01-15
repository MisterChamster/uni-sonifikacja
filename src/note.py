import numpy as np



class Note():
    sample_rate: int
    freq: float
    length_ms: int
    length_sec: float
    linspace: np.ndarray#[np.float64]
    tone: np.ndarray#IDK
    lowest_note_lambda_sample_count_roundup: int

    def __init__(self, in_s_rate: int, in_freq: float, in_len_ms: int) -> None:
        self.sample_rate = in_s_rate
        self.freq = in_freq
        self.length_ms = in_len_ms
        self.length_sec = in_len_ms / 1000

        self.linspace = np.linspace(0,
            self.length_sec,
            int(self.sample_rate * self.length_sec),
            endpoint=False)
        return

    #UNSAFE
    def calculate_tone(self) -> None:
        self.tone = np.sin(2 * np.pi * self.freq * self.linspace)
        return

    def get_tone(self) -> np.ndarray:
        return self.tone


    # Unsafe!
    def is_freq_rising_end(self) -> bool:
        if self.tone[-2] < self.tone[-1]:
            return True
        return False
