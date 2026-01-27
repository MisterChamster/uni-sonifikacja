import numpy as np



class Note():
    """
    Representation of a frequency (note) in time.

    Attributes:
        freq (float): Frequency.
        og_sample_amount (int): Original amount of samples.
        lowest_note_wavelen_samples_roundup (int): Amount of samples needed for calculating full wavelength of the lowest possible note.

        time_vector (np.ndarray[np.float64]): Constatnly rising function for calculation sine wave.
        tone (np.ndarray[np.float64] | None): Sine wave sample values array.
        last_freq (float | None): Last frequency of calculated tone.
        curr_sample_amount (int): Amount of samples in current tone.

        sample_rate (int): Sample rate of sound.
        similatiry_threshold (float): Threshold dictating when two frequencies are similar.
    """
    freq: float
    og_sample_amount: int
    lowest_note_wavelen_samples_roundup: int

    time_vector:        np.ndarray[np.float64]
    tone:               np.ndarray[np.float64] | None
    last_freq:          float | None
    curr_sample_amount: int

    sample_rate:            int = 44100
    similatiry_threshold: float = 0.03


# ================================== INITIAL ==================================
    def __init__(
        self,
        freq: float,
        og_sample_amount: int,
        lowest_note_wavelen_samples_roundup: int
    ) -> None:
        """
        Initialize Note instance.

        Args:
            freq: Frequency.
            og_sample_amount: Original amount of samples.
            lowest_note_wavelen_samples_roundup: Amount of samples needed for calculating full wavelength of the lowest possible note.
        """
        self.freq               = freq
        self.og_sample_amount   = og_sample_amount
        self.curr_sample_amount = og_sample_amount
        self.lowest_note_wavelen_samples_roundup = lowest_note_wavelen_samples_roundup

        self.tone      = None
        self.last_freq = None

        self.calculate_time_vector()
        return


# ============================== FUNCTIONALITIES ==============================
    def calculate_time_vector(self) -> None:
        """
        Calculate and set time vector of instance.
        """
        self.time_vector = np.arange(self.curr_sample_amount) / self.sample_rate
        return


    def calculate_tone(self) -> None:
        """
        Calculate and set tone of instance.

        Calculates a sine wave of an instance, then sets it and last frequency.
        """
        self.tone      = np.sin(2 * np.pi * self.freq * self.time_vector)
        self.last_freq = self.tone[-1]
        return


    def extend_with_lowest_note(self) -> None:
        """
        Extend time vector and tone with lowest note length.

        Sets up a new amount of samples to make tone from by adding a length of 
        the lowest possible note in samples. Then recalculates time vector and 
        tone of an instance.
        """
        self.curr_sample_amount += self.lowest_note_wavelen_samples_roundup
        self.calculate_time_vector()
        self.calculate_tone()
        return


    def cut_tone_to_match(
        self,
        is_freq_rising:      bool,
        prev_note_last_freq: float
    ) -> None:
        """
        Cut (extended) tone to match the previous sine wave.

        Cuts (extended) tone so that it matches the previous sine wave. For this, 
        it needs to:
        - Match its last frequency according to similarity threshold
        - Also be rising or falling

        Args:
            is_freq_rising (bool): Informs if last value of previous sine wave was higher than it's predecessor.
            prev_note_last_freq (float): Value of the last frequency present in previous sine wave.
        """
        if self.tone is None:
            raise TypeError("[ERROR] Code is written wrong. No tone has been calculated.")

        # TONE IS REVERSED FOR FAST POOPING
        reversed_tone = self.tone[::-1]
        for _ in range(self.lowest_note_wavelen_samples_roundup):
            # CRUCIAL
            # LOGIC REVERSED, BECAUSE TONE IS REVERSED
            is_reversed_rising: bool = (
                False
                if reversed_tone[-2] < reversed_tone[-1]
                else True)

            if not is_freq_rising and is_reversed_rising:
                reversed_tone = reversed_tone[:-1]
                continue
            elif is_freq_rising and not is_reversed_rising:
                reversed_tone = reversed_tone[:-1]
                continue
            elif not self.are_freqs_similar(prev_note_last_freq, reversed_tone[-1]):
                reversed_tone = reversed_tone[:-1]
                continue
            else:
                # print("They are similar!", prev_note_last_freq, reversed_tone[-1])
                break

        # DEATH HERE DEATH HERE DEATH HERE DEATH HERE DEATH HERE DEATH HERE DEATH HERE
        # HERE DEATH HERE DEATH HERE DEATH HERE DEATH HERE DEATH HERE DEATH HERE DEATH
        # DEATH HERE DEATH HERE DEATH HERE DEATH HERE DEATH HERE DEATH HERE DEATH HERE
        # If reversed tone length is lower then note length
        if len(reversed_tone) < self.og_sample_amount:
            print("ORIGINAL: ", self.og_sample_amount)
            print("NOT_OG!!: ", len(reversed_tone))
            raise ValueError("[ERROR] Code is written wrong. New tone length is shorter than it should.")

        popped_tone = reversed_tone[::-1]
        self.tone = popped_tone[:self.og_sample_amount]
        self.last_freq = self.tone[-1]

        self.curr_sample_amount = self.og_sample_amount
        self.calculate_time_vector()
        return


# =============================== BOOL CHECKERS ===============================
    # This does not check if tone is calculated for faster working
    # Check if tone is calculated before loop that uses this fun!
    def is_freq_rising_end(self) -> bool:
        """
        Check if tone is rising at the end.
        """
        if self.tone[-2] < self.tone[-1]:
            return True
        return False


    def are_freqs_similar(self, freq1: float, freq2: float) -> bool:
        """
        Check if notes are similar.

        Checks if notes are similar according to a similarity threshold.
        """
        # My approximation threshold will be 0.03. This value is arbitrary and
        # can be changed, but I think that it'll make little, if any, noticeable difference.
        # That value probably can be safely lowered l8r!
        if abs(freq1 - freq2) <= self.similatiry_threshold:
            return True
        return False


# ================================== GETTERS ==================================
    def get_tone(self) -> np.ndarray:
        """
        Get tone field of an instance.
        """
        return self.tone


    def get_last_freq(self) -> float:
        """
        Get last frequency field of an instance.
        """
        return self.last_freq
