import numpy as np

from .frame import Spectrum, Waveform

###################################################################################################


class FR(Spectrum):
    """
    Frequency response.
    """

    def __init__(self, camp: np.ndarray, samplerate: np.ndarray, nsamples: int = None):
        super().__init__(camp=camp, samplerate=samplerate, nsamples=nsamples)

    @classmethod
    def Wiener_filter(cls, original: Spectrum, fr: "FR", noise_psd: float):
        r"""
        Compute Wiener filter.

        Arguments:
            original: Spectrum of input signal.
            fr: frequency response of the system.
            noise_pdf: mean power spectral density of the noise E|\hat n(f)|^2.
        """
        # original, fr = Spectrum.equalize_size([original, fr])
        S = np.abs(original.camp) ** 2
        H = fr.camp
        return cls(
            camp=S * np.conj(H) / (np.abs(H) ** 2 * S + noise_psd),
            samplerate=fr.samplerate,
            nsamples=fr.nsamples,
        )

    @classmethod
    def by_example(
        cls,
        originals: list[Spectrum],
        observed: list[Spectrum],
        method="Hv",
        original_noise: float = 0,
        observed_noise: float = 0,
    ):
        # Hv estimator for single input, single output channel.
        # https://www.vibrationdata.com/tutorials_alt/FRF_measurements.pdf
        match len(originals), len(observed):
            case 1, m:
                originals = originals * m
            case n, 1:
                observed = observed * n
            case n, m:
                if n != m:
                    raise ValueError("Number of inputs do not match number of outputs.")
        GXF = Spectrum.mean(list(x * f for x, f in zip(observed, originals)))
        GFF = Spectrum.mean(list(f * f for f in originals))
        GXX = Spectrum.mean(list(x * x for x in observed))
        # Add noise contribution.
        GFF.camp += original_noise**2
        GXX.camp += observed_noise**2
        GXF.camp += original_noise * observed_noise
        # Compute frequency response.
        if method == "Hv":
            M = np.array([[GFF.camp, np.conj(GXF.camp)], [GXF.camp, GXX.camp]])
            M = np.moveaxis(M, (0, 1), (-2, -1))
            values, vectors = np.linalg.eigh(M)
            idx = np.argmin(values, axis=-1)
            V = vectors[..., idx]
            camp = -V[..., 0] / V[..., 1]
        elif method == "H1":
            camp = GXF.camp / GFF.camp
        elif method == "H2":
            camp = GXX.camp / np.conj(GXF.camp)
        else:
            raise ValueError("Unknown method")
        return cls(camp=camp, samplerate=GXF.samplerate, nsamples=GXF.nsamples)


###################################################################################################


class FIR(Waveform):
    """
    Finite impulse response.
    """

    def __init__(self, data: np.ndarray, samplerate: int):
        super().__init__(data=data, samplerate=samplerate)

    @classmethod
    def from_fr(cls, fr: FR) -> "FIR":
        data = np.fft.irfft(fr.camp, n=fr.nsamples, axis=0, norm="backward")
        return cls(data=data, samplerate=fr.samplerate)

    @classmethod
    def impulses(cls, location: list[int], amplitude: list[int], samplerate: int):
        N = np.max(location)
        data = np.zeros((N + 1, 1))
        for loc, a in zip(location, amplitude):
            data[loc] = a
        return cls(data=data, samplerate=samplerate)

    def apply(self, waveform: Waveform) -> Waveform:
        if self.samplerate != waveform.samplerate:
            raise ValueError("Samplerates do not match")
        if waveform.nchannels != self.nchannels and self.nchannels != 1:
            raise ValueError("Numbers of channels of filter and signal do not match.")
        result = []
        for cs in range(waveform.nchannels):
            cf = 0 if self.nchannels == 1 else cs
            channel_data = np.convolve(
                self.data[:, cf], waveform.data[:, cs], mode="full"
            )
            result.append(channel_data)
        data = np.stack(result, axis=1)
        return Waveform(
            data=data, samplerate=waveform.samplerate, first_sample=waveform.samplerate
        )


###################################################################################################
