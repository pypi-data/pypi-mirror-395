from functools import cached_property

import numpy as np

from .frame import Waveform

####################################################################################


class Basis:
    # Constructors.
    def __init__(self, basis, samplerate):
        self.basis = basis
        self.samplerate = samplerate

    @classmethod
    def linear_chirp(
        cls, f1: float, f2: float, samplerate: float, length_t: float, phi: float = 0
    ):
        length = int(length_t * samplerate)
        t = np.arange(length) / samplerate
        c = (f2 - f1) / length_t
        alpha = phi + np.pi * c * t**2 + 2 * np.pi * f1 * t
        basis = np.stack([np.cos(alpha), -np.sin(alpha)], axis=1)
        return cls(basis=basis, samplerate=samplerate)

    @classmethod
    def exp_chirp(
        cls, f1: float, f2: float, samplerate: float, length_t: float, phi: float = 0
    ):
        length = int(length_t * samplerate)
        t = np.arange(length) / samplerate
        k = f2 / f1
        alpha = phi + 2 * np.pi * f1 / np.log(k) * length_t * k ** (t / length_t)
        basis = np.stack([np.cos(alpha), -np.sin(alpha)], axis=1)
        return cls(basis=basis, samplerate=samplerate)

    @classmethod
    def sine_wave(cls, frequency: float, samplerate: float, length_t: float):
        length = int(length_t * samplerate)
        alpha = 2 * np.pi * frequency / samplerate * np.arange(length)
        basis = np.stack([np.cos(alpha), -np.sin(alpha)], axis=1)
        return cls(basis=basis, samplerate=samplerate)

    # Basis modification.
    def with_sine_envelope(self):
        x = np.arange(self.nsamples) / self.nsamples
        envelope = np.sin(np.pi * x)
        data = self.basis * envelope[:, None]
        return Basis(basis=data, samplerate=self.samplerate)

    def fade(self, length_t, fadein=True, fadeout=True):
        data = self.basis.copy()
        nsamples = int(length_t * self.samplerate)
        x = np.arange(nsamples) / nsamples
        envelope = np.sin(0.5 * np.pi * x)
        if fadein:
            data[:nsamples] *= envelope[:, None]
        if fadeout:
            data[-nsamples:] *= envelope[::-1, None]
        return Basis(basis=data, samplerate=self.samplerate)

    def with_constant(self):
        data = np.concatenate([self.basis, np.ones((self.nsamples, 1))], axis=1)
        return Basis(basis=data, samplerate=self.samplerate)

    # Properties
    @property
    def nsamples(self):
        return self.basis.shape[0]

    @property
    def dim(self):
        return self.basis.shape[1]

    @cached_property
    def gram(self):
        return np.sum(self.basis[:, None, :] * self.basis[:, :, None], axis=0)

    @cached_property
    def igram(self):
        return np.linalg.inv(self.gram)

    # Transform to other types.
    def to_waveform(self) -> Waveform:
        return Waveform(data=self.basis, samplerate=self.samplerate)

    @classmethod
    def from_waveform(cls, waveform: Waveform) -> "Basis":
        return Basis(basis=waveform.data, samplerate=waveform.samplerate)

    def at(self, coef: np.ndarray, **kwargs) -> Waveform:
        coef = np.asarray(coef)
        data = (self.basis @ coef)[:, None]
        return Waveform(data=data, samplerate=self.samplerate, **kwargs)

    # Operations on numpy array.
    def lstsq_np(self, data):
        assert data.ndim == 2 and data.shape[0] == self.nsamples
        proj = np.sum(data[:, None, :] * self.basis[:, :, None], axis=0)
        x = self.igram @ proj
        return x

    def apply_np(self, x):
        return self.basis @ x

    # Convolution.
    def convolve_np(self, data: np.ndarray):
        M, C = data.shape
        N, B = self.basis.shape
        assert M >= N
        R = M - N + 1
        proj = np.empty((R, C, B), dtype=data.dtype)
        for c in range(C):
            for b in range(B):
                proj[:, c, b] = np.correlate(data[:, c], self.basis[:, b], mode="valid")
        # for n in range(R):
        #     proj[n] = np.sum(self.basis[:,None,:]*data[n:n+N,:,None],axis=0)
        return np.einsum("ij,tcj->tci", self.igram, proj)
