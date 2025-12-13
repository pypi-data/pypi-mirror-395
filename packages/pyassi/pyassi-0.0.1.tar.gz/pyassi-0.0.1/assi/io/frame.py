from functools import cached_property

import numpy as np
import soundfile as sf

from .window import Window

####################################################################################################


class AbstractFrame:
    pass


####################################################################################################


class Spectrum(AbstractFrame):
    # Constructors.
    def __init__(self, camp: np.ndarray, samplerate: int, nsamples: int = None):
        self.camp = camp
        self.samplerate = samplerate
        self.nsamples = nsamples if nsamples is not None else 2 * (camp.shape[0] - 1)

    @classmethod
    def from_pcm(cls, waveform: "Waveform") -> "Spectrum":
        camp = np.fft.rfft(waveform.data, n=None, axis=0, norm="backward")
        return cls(
            camp=camp, samplerate=waveform.samplerate, nsamples=waveform.nsamples
        )

    @classmethod
    def mean(cls, spectra: list["Spectrum"]) -> "Spectrum":
        return Spectrum.sum(spectra) / len(spectra)

    @classmethod
    def sum(cls, spectra: list["Spectrum"]) -> "Spectrum":
        if len(spectra) == 0:
            raise ValueError("At least one spectrum should be provided.")
        r = spectra[0]
        for s in spectra[1:]:
            r = r + s
        return r

    # Properties.
    @property
    def nfreq(self) -> int:
        return self.camp.shape[0]

    @cached_property
    def freq(self) -> np.ndarray:
        return np.fft.rfftfreq(n=self.nsamples, d=1 / self.samplerate)

    @cached_property
    def amp(self) -> np.ndarray:
        return np.abs(self.camp)

    @cached_property
    def phase(self) -> np.ndarray:
        return np.angle(self.camp)

    # Conversion.
    def to_waveform(self, **kwargs) -> "Waveform":
        data = np.fft.irfft(self.camp, n=self.nsamples, axis=0, norm="backward")
        return Waveform(data=data, samplerate=self.samplerate, **kwargs)

    # Utilities.
    # def expand(self, nfreq:int, nsamples:int) -> 'Spectrum':
    #     if nsamples<=self.nsamples:
    #         return self
    #     camp = np.zeros((nfreq,)+self.camp.shape[1:], dtype=np.complex128)
    #     camp[:self.nfreq] = self.camp
    #     return Spectrum(camp=camp, samplerate=self.samplerate, nsamples=nsamples)

    # def expand_as(self, o:'Spectrum') -> 'Spectrum':
    #     return self.expand(nfreq=o.nfreq, nsamples=o.nsamples)

    # @staticmethod
    # def equalize_size(spectra:list['Spectrum']) -> list['Spectrum']:
    #     idx = np.argmax(list(s.nsamples for s in spectra))
    #     return list(s.expand(nfreq=spectra[idx].nfreq, nsamples=spectra[idx].nsamples) for s in spectra)

    # Operators.
    def __add__(self, other) -> "Spectrum":
        if isinstance(other, Spectrum):
            # a, b = Spectrum.equalize_size([self,other])
            a, b = self, other
            if a.samplerate != b.samplerate:
                raise ValueError("Sampling rates do not match")
            return Spectrum(
                camp=a.camp + b.camp, samplerate=a.samplerate, nsamples=a.nsamples
            )
        return NotImplemented

    def __mul__(self, other) -> "Spectrum":
        if isinstance(other, Spectrum):
            # a, b = Spectrum.equalize_size([self,other])
            a, b = self, other
            if a.samplerate != b.samplerate:
                raise ValueError("Sampling rates do not match")
            return Spectrum(
                camp=a.camp * np.conj(b.camp),
                samplerate=a.samplerate,
                nsamples=a.nsamples,
            )
        if np.isscalar(other):
            return Spectrum(
                camp=self.camp * other,
                samplerate=self.samplerate,
                nsamples=self.nsamples,
            )
        return NotImplemented

    def __truediv__(self, other) -> "Spectrum":
        if np.isscalar(other):
            return self * (1 / other)
        return NotImplementedError


####################################################################################################


class PCMArray(AbstractFrame):
    def __init__(
        self,
        data: np.ndarray,
        samplerate: int,
        first_sample: int = None,
        t0: float = None,
    ):
        self.data = data
        self.samplerate = samplerate

        match first_sample, t0:
            case None, None:
                self.first_sample = 0
            case x, None:
                self.first_sample = x
            case None, t:
                self.first_sample = int(self.samplerate * t)
            case _x, _t:
                raise ValueError(
                    "`first_sample` and `t0` arguments are mutually exclusive."
                )

        assert isinstance(self.data, np.ndarray)

    # Properties
    @property
    def nsamples(self):
        return self.data.shape[0]

    @property
    def nchannels(self):
        return self.data.shape[1]

    @property
    def t0(self):
        return self.first_sample / self.samplerate


####################################################################################################


class Waveform(PCMArray):
    def __init__(self, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        if self.data.ndim != 2:
            raise ValueError("Waveform data must have axis (sample,channel)")

    # Constructors
    @classmethod
    def concatenate(cls, waveforms: list["Waveform"], end_to_end=True):
        # Check arguments.
        N = len(waveforms)
        if N == 0:
            raise ValueError("At least one segment is expected.")
        for wave in waveforms:
            if wave.samplerate != waveforms[0].samplerate:
                raise ValueError("All segments must have the same samplerate.")
        # Make index of all segments.
        start = np.empty(N, dtype=np.int64)
        end = np.empty(N, dtype=np.int64)
        for n, wave in enumerate(waveforms):
            start[n] = wave.first_sample
            end[n] = start[n] + wave.nsamples
        # If first_sample of every segment is relative to the previous segment,
        if end_to_end:
            # update positions to global one.
            for n in range(1, start.shape[0]):
                s = end[n - 1]
                start[n] += s
                end[n] += s
        nchannels = max(wave.nchannels for wave in waveforms)
        # Find final result position and length.
        first_sample = np.min(start)
        nsamples = np.max(end) - first_sample
        start -= first_sample
        end -= first_sample
        # Allocate buffer and save all components.
        data = np.zeros(
            (nsamples, nchannels),
        )
        for n, wave in enumerate(waveforms):
            data[start[n] : end[n], : wave.nchannels] += wave.data
        return Waveform(
            data=data, samplerate=waveforms[0].samplerate, first_sample=first_sample
        )

    @classmethod
    def silence_like(cls, other: "Waveform"):
        assert isinstance(other, Waveform)
        return cls(
            data=np.zeros_like(other.data),
            samplerate=other.samplerate,
            first_sample=other.first_sample,
        )

    @classmethod
    def sin_wave(cls, omega, samplerate=48000, length_t=1, first_sample=0):
        nsamples = int(samplerate * length_t)
        alpha = 2 * np.pi * omega / samplerate * np.arange(nsamples)
        data = np.sin(alpha)[:, None]
        return cls(data=data, samplerate=samplerate, t0=first_sample)

    @classmethod
    def white_noise(cls, samplerate=48000, length_t=1, std=0.25):
        nsamples = int(samplerate * length_t)
        data = np.random.normal(size=(nsamples,), scale=std)[:, None]
        return cls(data=data, samplerate=samplerate, t0=0)

    # File IO
    @classmethod
    def load(cls, filename, **kwargs):
        data, samplerate = sf.read(filename, always_2d=True)
        return cls(data=data, samplerate=samplerate)

    def save(self, filename):
        sf.write(filename, data=self.data, samplerate=self.samplerate)

    # Properties
    @cached_property
    def time(self):
        return self.t0 + np.arange(self.nsamples) / self.samplerate

    @property
    def length(self):
        return self.nsamples / self.samplerate

    # Operators.
    def __str__(self):
        return f"PCM {self.length:.4f} seconds at {self.samplerate} Hz {self.nchannels} channels"

    def __and__(self, other):
        if isinstance(other, Waveform):
            return self.merge_channels(other)
        return NotImplemented

    # Extract data.
    def __getitem__(self, key):
        if isinstance(key, slice):
            a = key.start if key.start is not None else 0
            b = key.stop if key.stop is not None else -1
            s = key.step if key.step is not None else 1
            return self.crop(a=a, b=b, s=s)
        raise KeyError(f"Unsupported key type {type(key)}")

    def channel(self, channels: list[int]) -> "Waveform":
        if isinstance(channels, int):
            channels = [channels]
        return Waveform(
            data=self.data[:, channels],
            samplerate=self.samplerate,
            first_sample=self.first_sample,
        )

    # Editing.
    def repeat_channels(self, count: int):
        return self.__class__(
            data=np.repeat(self.data, count, axis=1),
            samplerate=self.samplerate,
            first_sample=self.first_sample,
        )

    def merge_channels(self, other: "Waveform"):
        assert self.samplerate == other.samplerate
        assert self.t0 == other.t0
        return Waveform(
            data=np.stack([self.data, other.data], axis=-1),
            samplerate=self.samplerate,
            first_sample=self.first_sample,
        )

    def normalize(self, max=1.0):
        return Waveform(
            data=self.data * (max / self.get_amplitude_peak()),
            samplerate=self.samplerate,
            first_sample=self.first_sample,
        )

    def crop(self, a=0, b=-1, s=1):
        return Waveform(
            data=self.data[a:b:s], t0=self.time[a], samplerate=self.samplerate / s
        )

    def crop_t(self, ta, tb):
        return self.crop(a=self.to_sample(ta), b=self.to_sample(tb))

    def trim_silence(
        self, threshold, pad: int = 0, initial: bool = True, final: bool = True
    ):
        a = self.get_initial_silence_length(threshold) if initial else 0
        b = self.get_final_silence_length(threshold) if final else self.nsamples
        return self[max(0, a - pad) : min(self.nsamples, b + pad)]

    def add_white_noise(self, std: float):
        data = self.data + np.random.normal(
            size=(self.nsamples, self.nchannels), scale=std
        )
        return Waveform(
            data=data, samplerate=self.samplerate, first_sample=self.first_sample
        )

    # Get info,
    def get_amplitude_peak(self):
        return np.max(np.abs(self.data))

    def get_amplitude_rms(self):
        return np.sqrt(np.mean(self.data**2))

    @cached_property
    def volume(self):
        return np.sqrt(np.sum(self.data**2, axis=1))  # Sum over all channels

    def to_sample(self, t):
        return int((t - self.t0) * self.samplerate)

    def get_initial_silence_length(self, threshold):
        idx = np.argmax(self.volume > threshold)
        return idx

    def get_final_silence_length(self, threshold):
        idx = np.argmax(self.volume[::-1] > threshold)
        return self.nsamples - idx

    @cached_property
    def spec(self):
        return Spectrum.from_pcm(waveform=self)

    def expand(self, nsamples: int) -> "PCMArray":
        if nsamples <= self.nsamples:
            return self
        data = np.zeros((nsamples,) + self.data.shape[1:], dtype=self.data.dtype)
        data[: self.nsamples] = self.data
        return Waveform(data=data, samplerate=self.samplerate)

    def expand_as(self, o: "PCMArray") -> "PCMArray":
        return self.expand(nsamples=o.nsamples)


####################################################################################################


class PCMFrame(Waveform):
    def __init__(self, *vargs, np_window: np.ndarray = None, **kwargs):
        super().__init__(*vargs, **kwargs)
        self.np_window = np_window
        assert isinstance(self.np_window, np.ndarray)

    @classmethod
    def from_waveform(self, waveform: Waveform, window: Window):
        np_window = window.in_time_domain(waveform.nsamples)
        return PCMFrame(
            data=waveform.data * np_window[:, None],
            samplerate=waveform.samplerate,
            first_sample=waveform.first_sample,
            np_window=np_window,
        )
