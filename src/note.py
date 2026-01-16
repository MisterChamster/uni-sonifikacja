import numpy as np
from src.utils import Utils



class Note():
    sample_rate: int
    freq:        float
    length_ms:   int
    lowest_note_wavelen_samples_roundup: int

    linspace:  np.ndarray#[np.float64]
    tone:      np.ndarray | None#IDK tone val types
    last_freq: float | None
    length_samples: int

    #OK
    def __init__(
        self,
        sample_rate: int,
        freq:        float,
        length_ms:   int,
        lowest_note_wavelen_samples_roundup: int
    ) -> None:
        self.sample_rate = sample_rate
        self.freq = freq
        self.length_ms = length_ms
        self.lowest_note_wavelen_samples_roundup = lowest_note_wavelen_samples_roundup

        self.last_freq = None
        self.tone      = None

        self.calculate_linspace_and_lensamples()
        return


    # OK
    def calculate_linspace_and_lensamples(self) -> None:
        len_in_sec = self.length_ms / 1000
        self.linspace = np.linspace(0,
            len_in_sec,
            int(self.sample_rate * len_in_sec),
            endpoint=False)
        self.length_samples = self.sample_rate * len_in_sec
        return


    # OK
    def calculate_tone(self) -> None:
        self.tone = np.sin(2 * np.pi * self.freq * self.linspace)
        self.last_freq = self.tone[-1]
        return


    # OK
    def extend_with_lowest_note(self) -> None:
        lowest_wavelen_sec: float = self.sample_rate / self.lowest_note_wavelen_samples_roundup
        lowest_wavelen_ms:  float = lowest_wavelen_sec / 1000
        self.length_ms += lowest_wavelen_ms

        self.calculate_linspace_and_lensamples()
        self.calculate_tone()
        return


    def cut_tone_to_match(
        self,
        is_freq_rising: bool,
        last_freq: float,
        longest_wavelen_in_samples: int
    ) -> None:
        # TONE IS REVERSED FOR FAST POPPING
        reversed_tone = self.tone[::-1]
        if not self.tone:
            raise TypeError("[ERROR] Code is written wrong. No tone is calculated.")
        for _ in range(longest_wavelen_in_samples):
            if not is_freq_rising and self.is_freq_rising_end():
                reversed_tone.pop()
                continue
            elif is_freq_rising and not self.is_freq_rising_end():
                reversed_tone.pop()
                continue
            elif not self.are_freqs_similar(last_freq, self.tone[-1]):
                reversed_tone.pop()
                continue
            else:
                break
            # NEED NOTE LEN IN SAMPLES VAR
            # If reversed tone length is lower then note length - error

            # FREQS ARE SIMILAR
            popped_tone = reversed_tone[::-1]
            # HERE, we need required and current len in samples


            # If not are similar
            # COME BACK HERE
            # My approximation threshold will be 0.05. This value can be changed,
            # but I think that it'll make little, if any, noticeable difference.
            # That value probably can be safely lowered l8r!
        return


# =============================== BOOL CHECKERS ===============================
    # This does not check if tone is calculated for faster working
    # Check if tone is calculated before loop that uses this fun!
    # OK
    def is_freq_rising_end(self) -> bool:
        if self.tone[-2] < self.tone[-1]:
            return True
        return False


    # OK
    def are_freqs_similar(freq1: float, freq2: float) -> bool:
        threshold_var = 0.05
        if abs(freq1 - freq2) <= threshold_var:
            return True
        return False


# ================================== GETTERS ==================================
    def get_tone(self) -> np.ndarray:
        return self.tone


    def get_last_freq(self) -> float:
        return self.last_freq
