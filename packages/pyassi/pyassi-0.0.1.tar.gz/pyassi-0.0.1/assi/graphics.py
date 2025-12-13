# import numpy as np
import matplotlib.pyplot as plt

from .io.frame import Spectrum, Waveform

####################################################################################


def plot(obj, **kwargs):
    if isinstance(obj, Waveform):
        return plot_waveform(obj, **kwargs)
    raise TypeError(f"Unsupported type {type(obj)}")


####################################################################################


def plot_waveform(
    waveform: Waveform,
    fig=None,
    ax=None,
    budget=100000,
    ls=None,
    hidex=False,
    hidey=False,
):
    if fig is None:
        fig, ax = plt.subplots(figsize=(20, 5))
    skip = max(1, waveform.nsamples // budget)
    rdata = waveform.data[::skip]
    ax.axhline(0, color="k", ls=":", lw=0.5)
    if ls is None:
        ls = "," if rdata.shape[0] > 5000 else "-"
    ax.plot(waveform.time[::skip], rdata, ls)
    if not hidex:
        ax.set_xlabel("Time (sec)")
    if not hidey:
        ax.set_ylabel("Amplitude")
    ax.set_xlim(waveform.t0, waveform.t0 + waveform.length)
    # ax.set_ylim([-1,1])
    return fig, ax


####################################################################################


def plot_spectrum(spec: Spectrum, fig=None, axes=None, ls=None, logy=False):
    if fig is None:
        fig, axes = plt.subplots(
            ncols=2, figsize=(20, 5), sharex=True, layout="compressed"
        )
    if ls is None:
        ls = "," if spec.nfreq > 5000 else "-"
    freq = spec.freq
    ax = axes[0]
    ax.plot(freq, spec.amp, ls)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude")

    if logy:
        ax.set_yscale("log")

    ax = axes[1]
    ax.plot(freq, spec.phase, ls)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Phase")
    ax.set_xlim(freq[0], freq[-1])

    return fig, axes
