import numpy as np
from nicegui import ui

from ..io.frame import PCMFrame, Spectrum
from ..io.stream import AbstractStream, PCMStreamPointer
from ..io.util import camp_to_rgb
from ..io.window import HannWindow
from .log import logger
from .source import Source

##################################################################################
# Classes implementing modes of operation.


class Mode:
    NAME = "Abstract"

    def __init__(self):
        self.stream: AbstractStream = None
        self.pointer: PCMStreamPointer = None
        self._source: Source = None

    def attach(self, source: Source):
        logger.debug(f"Mode.attach({source}=)")
        self._source = source
        self.pointer = None
        self.stream = None
        if source is None:
            return
        self.stream = source.stream
        if self.stream is None:
            return
        self.pointer = self.stream.new_pointer()
        self._samples_read = 0

    def detach(self):
        logger.debug("Mode.detach()")
        if self.pointer is not None:
            self.pointer.detach()
        self.pointer = None
        self.stream = None
        self.source = None

    def init_interface(self):
        logger.debug("Mode.init_interface()")

    def adapt_interface(self):
        logger.debug("Mode.adapt_interface()")

    def process_input(self, nsamples: int):
        raise NotImplementedError

    def redraw(self):
        pass

    @property
    def nsamples_to_prebuffer(self):
        return 0


##################################################################################


class DummyMode(Mode):
    NAME = "Dummy"

    def __init__(self):
        super().__init__()

    def init_interface(self):
        logger.debug("DummyMode.init_interface()")
        ui.label("Dummy mode")

    def process_input(self, nsamples: int):
        if self.pointer is None:
            return
        self.pointer.skip(nsamples)


##################################################################################


class BasicMode(Mode):
    NAME = "BasicMode"

    def __init__(self):
        super().__init__()
        self.plot = None
        self.ax = None
        self._samples_to_read = 0
        self._iframelen = None

    def attach(self, source: Source):
        super().attach(source)
        if self._source is not None and self._iframelen is not None:
            self._source.announce_natural_step(self._iframelen.value)

    def init_ui_left_column(self):
        self._iyscale = ui.select(
            options={
                1: "1x",
                0.5: "2x",
                0.25: "4x",
                0.1: "10x",
                0.05: "20x",
                0.02: "50x",
                0.01: "100x",
                0.005: "200x",
            },
            label="y-scale",
            value=1,
            on_change=self.on_yscale,
        ).classes("w-full")

        self._iframelen = ui.select(
            options={1: "1sec", 0.1: "100ms", 0.05: "50ms", 0.02: "20ms", 0.01: "10ms"},
            label="Time scale",
            value=0.05,
            on_change=self.on_framelen,
        ).classes("w-full")

    def init_figure(self):
        with ui.pyplot(figsize=(10, 5), close=False) as self.plot:
            self.ax = self.plot.fig.add_subplot()

    def init_interface(self):
        logger.debug("BasicMode.init_interface()")
        with ui.row().classes("w-full no-wrap"):
            with ui.column().classes("w-32 no-wrap"):
                self.init_ui_left_column()
            self.init_figure()

    def _receive_frame(self, nsamples: int, samples_per_frame: int, skip: int):
        if self.pointer is None:
            return
        self._samples_to_read += nsamples
        # logger.debug(f"BasicMode.process_input {nsamples=} {self._samples_to_read=} {samples_per_frame=}")

        # Read specified number of samples.
        if self._samples_to_read < samples_per_frame:  # Not enough data.
            return
        skip = samples_per_frame
        shift = (self._samples_to_read - samples_per_frame) // skip
        self.pointer.skip(shift * skip)
        self._samples_to_read -= shift * skip
        data = self.pointer.extract(samples_per_frame)
        if data is not None:  # If not end of the stream
            self.pointer.skip(skip)
            self._samples_to_read -= skip
        return data

    def on_yscale(self, msg):
        _scale = msg.value

    @property
    def nsamples(self):
        if self.stream is None:
            return 1
        return int(self.stream.samplerate * self._iframelen.value)

    def on_framelen(self, msg):
        framelen = msg.value
        if self._source is not None:
            self._source.announce_natural_step(framelen)

    @property
    def nsamples_to_prebuffer(self):
        return self.nsamples + 1


##################################################################################


class OscilloscopeMode(BasicMode):
    NAME = "Oscilloscope"

    def __init__(self):
        super().__init__()
        self.lines = None
        self._data = None

    def init_ui_left_column(self):
        logger.debug("OscilloscopeMode.init_ui_left_column()")
        super().init_ui_left_column()
        self._trigger = ui.select(
            options={"none": "None", "rising": "Rising edge"},
            label="Trigger",
            value="none",
        ).classes("w-full")

    def adapt_interface(self):
        logger.debug("OscilloscopeMode.adapt_interface()")
        if self.plot is None:
            logger.error("init_interface should be called before adapt_interface")
            return
        if self.pointer is None:  # Not connected to input.
            return
        samplerate = self.stream.samplerate
        nchannels = self.stream.nchannels

        time = np.arange(self.nsamples) / samplerate
        self._data = np.zeros((self.nsamples, nchannels))
        with self.plot:
            # Remove old line.
            if self.lines is not None:
                self.ax.clear()
            # Set new parameters.
            yscale = self._iyscale.value
            self.ax.set_ylim(-yscale, yscale)
            self.ax.set_xlim(0, self._iframelen.value)
            self.lines = self.ax.plot(time, self._data, ls="-", lw=0.2)
            self.ax.set_xlabel("Time (sec)")
            self.ax.set_ylabel("Amplitude")
        ui.update(self.plot)

    def process_input(self, nsamples: int):
        data = self._receive_frame(
            nsamples=nsamples, samples_per_frame=self.nsamples, skip=self.nsamples
        )
        if data is None:
            return  # Nothing do proceed.

        # Save data.
        self._data = data
        # Align signals if a trigger is specified.
        trigger = self._trigger.value
        if trigger == "rising":
            # Find rising edge.
            ch = 0
            sgn = self._data[:, ch] >= 0
            sgn_change = np.logical_and(sgn[1:], np.logical_not(sgn[:-1]))
            idx = np.argmax(sgn_change)
            idx = int(idx)
            # Remove part of the signal.
            self._data = self._data[idx:]

    def redraw(self):
        # logger.debug(f"BasicMode.redraw() {self._data is None=}")
        if self.pointer is None or self._data is None:
            return
        if self.lines is None:
            logger.error("BasicMode.adapt_interface was not called.")
            return

        with self.plot:
            # ls = self._linestyle.value
            nsamples = self._data.shape[0]
            time = np.arange(nsamples) / self.stream.samplerate
            for c, line in enumerate(self.lines):
                y = self._data[:, c]
                line.set_data(time, y)
                # line.set_linestyle(ls)
        ui.update(self.plot)
        # self._data = None
        # logger.debug("BasicMode.redraw() done")

    def on_yscale(self, msg):
        scale = msg.value
        if self.ax is not None:
            self.ax.set_ylim(-scale, scale)

    def on_framelen(self, msg):
        super().on_framelen(msg)
        framelen = msg.value
        if self.ax is not None:
            self.ax.set_xlim(0, framelen)


##################################################################################


class SpectrumPlugin:
    NAME = "???"

    def __init__(self, parent: BasicMode):
        assert isinstance(parent, SpectrumMode)
        self._parent = parent
        self._lines = None

    def adapt(self, spectrum):
        raise NotImplementedError

    def redraw(self, spectrum):
        raise NotImplementedError

    def stop(self):
        pass

    @property
    def samplerate(self):
        return self._parent.stream.samplerate

    def on_yscale(self, scale: float):
        pass


class MagnitudeSpectrumPlugin(SpectrumPlugin):
    NAME = "Magnitude"

    def adapt(self, spectrum):
        # Clear
        self._parent.ax.clear()
        # Precompute constants.
        nfreq = spectrum.shape[0]
        freqs = np.linspace(0, self.samplerate / 2, nfreq)

        # Set new parameters.
        yscale = self._parent._iyscale.value
        ax = self._parent.ax
        ax.set_ylim(1e-6, yscale)
        ax.set_xlim(0, freqs[-1])
        self._lines = self._parent.ax.plot(
            freqs, self.compute(spectrum), ls="-", lw=0.2
        )
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Amplitude")
        ax.set_yscale("log")

    def redraw(self, spectrum):
        nfreq = spectrum.shape[0]
        freqs = np.linspace(0, self._parent.stream.samplerate / 2, nfreq)
        y = self.compute(spectrum)
        for c, line in enumerate(self._lines):
            line.set_data(freqs, y[:, c])

    def compute(self, spectrum):
        nfreq = spectrum.shape[0]
        return np.abs(spectrum) / (2 * nfreq)

    def on_yscale(self, scale: float):
        ax = self._parent.ax
        if ax is not None:
            ax.set_ylim(0, scale)


class PhaseSpectrumPlugin(SpectrumPlugin):
    NAME = "Phase"

    def adapt(self, spectrum):
        # Clear
        self._parent.ax.clear()
        # Precompute constants.
        nfreq = spectrum.shape[0]
        freqs = np.linspace(0, self.samplerate / 2, nfreq)

        # Set new parameters.
        ax = self._parent.ax
        ax.set_ylim(-np.pi, np.pi)
        ax.set_xlim(0, freqs[-1])
        self._lines = self._parent.ax.plot(
            freqs, self.compute(spectrum), ls="-", lw=0.2
        )
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Phase (rad)")
        ax.set_yscale("linear")

    def redraw(self, spectrum):
        y = self.compute(spectrum)
        for c, line in enumerate(self._lines):
            line.set_ydata(y[:, c])

    def compute(self, spectrum):
        return np.angle(spectrum)


class NyquistSpectrumPlugin(SpectrumPlugin):
    NAME = "Nyquist"

    def adapt(self, spectrum):
        # Clear
        self._parent.ax.clear()
        # Precompute constants.

        # Set new parameters.
        yscale = self._parent._iyscale.value
        ax = self._parent.ax
        ax.set_ylim(-yscale, yscale)
        ax.set_xlim(-yscale, yscale)
        self._lines = self._parent.ax.plot(*self.get_xy(spectrum), ls="-", lw=0.2)
        ax.set_xlabel("Real")
        ax.set_ylabel("Imag")
        ax.set_xscale("linear")
        ax.set_yscale("linear")

    def get_xy(self, spectrum):
        mx = 2 * spectrum.shape[0]
        return np.real(spectrum) / mx, np.imag(spectrum) / mx

    def redraw(self, spectrum):
        x, y = self.get_xy(spectrum)
        for c, line in enumerate(self._lines):
            line.set_data(x[:, c], y[:, c])

    def on_yscale(self, scale: float):
        ax = self._parent.ax
        if ax is not None:
            ax.set_xlim(-scale, scale)
            ax.set_ylim(-scale, scale)


class RelativeSpectrumPlugin(NyquistSpectrumPlugin):
    NAME = "Relative phase"

    def get_xy(self, spectrum):
        compensation = np.exp(-1j * np.angle(spectrum[:, 0]))
        spec = spectrum * compensation[:, None]
        mx = 2 * spectrum.shape[0]
        return np.real(spec) / mx, np.imag(spec) / mx


###


class SpectrumMode(BasicMode):
    NAME = "Spectrum"
    PLUGINS = [
        MagnitudeSpectrumPlugin,
        PhaseSpectrumPlugin,
        NyquistSpectrumPlugin,
        RelativeSpectrumPlugin,
    ]

    def __init__(self):
        super().__init__()
        self._spectrum = None
        self._plugin: SpectrumPlugin = None
        self._time_in_samples = 0

    def adapt_interface(self):
        logger.debug("SpectrumMode.adapt_interface()")
        if self.plot is None:
            logger.error("init_interface should be called before adapt_interface")
            return
        if self.pointer is None:  # Not connected to input.
            return
        nchannels = self.stream.nchannels
        nsamples = self.nsamples
        nfreq = nsamples // 2 + 1 if nsamples % 2 == 0 else (nsamples + 1) // 2

        self._spectrum = np.zeros((nfreq, nchannels))
        if self._plugin is not None:
            with self.plot:
                self._plugin.adapt(self._spectrum)

        ui.update(self.plot)

    def attach(self, source):
        super().attach(source)
        self._time_in_samples = 0

    def process_input(self, nsamples: int):
        samples_per_frame = self.nsamples
        data = self._receive_frame(
            nsamples=nsamples, samples_per_frame=samples_per_frame, skip=self.nsamples
        )
        if data is None:
            return
        self._time_in_samples += data.shape[0]

        # Save data.
        np_window = HannWindow().in_time_domain(nsamples=samples_per_frame)
        frame = PCMFrame(
            data=data, samplerate=self.pointer.stream.samplerate, np_window=np_window
        )
        self._spectrum = Spectrum.from_pcm(frame).camp

        if self._ialign.value:
            self.align_spectrum()

    def align_spectrum(self):
        nfreq = self._spectrum.shape[0]
        samples_per_frame = self.nsamples
        t = self._time_in_samples / samples_per_frame
        compensation = np.exp(-2j * np.pi * t * np.arange(nfreq))
        self._spectrum *= compensation[:, None]

    def redraw(self):
        # logger.debug(f"BasicMode.redraw() {self._data is None=}")
        if self.pointer is None or self._spectrum is None:
            return

        if self._plugin is not None:
            with self.plot:
                self._plugin.redraw(self._spectrum)
        ui.update(self.plot)

    def on_yscale(self, msg):
        scale = msg.value
        if self._plugin is not None:
            self._plugin.on_yscale(scale)

    def init_ui_left_column(self):
        logger.debug("SpectrumMode.init_ui_left_column()")
        super().init_ui_left_column()
        names = list(p.NAME for p in self.PLUGINS)

        self._ialign = ui.checkbox(
            text="Align phases",
            value=False,
        )

        self._iplugin = ui.select(
            options=names,
            on_change=self.on_plugin_select,
            value=names[0],
            label="Plot type",
        )
        self.on_plugin_select()

    def on_plugin_select(self, msg=None):
        logger.debug(
            f"SpectrumMode.on_plugin_select({'' if msg is None else msg.value})"
        )
        name = self._iplugin.value
        plugin = None
        # Find plugin.
        for p in self.PLUGINS:
            if name == p.NAME:
                plugin = p
                break
        # If unknown name.
        if plugin is None:
            logger.error(f"Unknown plugin name: {name}")
            return
        # Deinitialize previous plugin.
        if self._plugin is not None:
            self._plugin.stop()
        # Create new plugin.
        self._plugin = plugin(self)
        # Prepare UI.
        self.adapt_interface()


##################################################################################


class SpectrogramMode(Mode):
    NAME = "Spectrogram"

    def __init__(self):
        super().__init__()
        # Graphics elements.
        self.plot = None
        self.ax = None
        self.image = None
        # UI controlled parameters.
        self._nframes = 100
        # History data.
        self.spectra = None
        self._nsamples = None
        self._samples_to_read = 0

    def create_spectra(self):
        if self.stream is None:
            return
        nchannels = self.stream.nchannels
        nfreq = int(self.nsamples / 2)
        self.spectra = np.zeros(
            shape=(self._nframes, nfreq, nchannels), dtype=np.complex64
        )

    def attach(self, source: Source):
        super().attach(source)
        self.create_spectra()
        # Update UI
        if self.stream is not None:
            self._ichannel.options = list(range(self.stream.nchannels))
            ui.update(self._ichannel)
        if self._source is not None:
            self._source.announce_natural_step(self._istep.value)

    def detach(self):
        super().detach()
        self.spectra = None

    # UI
    def init_interface(self):
        logger.debug("SpectrogramMode.init_interface()")
        with ui.row().classes("w-full no-wrap"):
            with ui.column().classes("w-32 no-wrap"):
                TSIZES = {
                    1: "1sec",
                    0.5: "500ms",
                    0.2: "200ms",
                    0.1: "100ms",
                    0.05: "50ms",
                    0.025: "25ms",
                    0.01: "10ms",
                }
                XAMP = {
                    v: f"x{v}"
                    for v in [0.1, 0.5, 1.0, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
                }
                self._ixamp = ui.select(
                    options=XAMP,
                    label="Amplitude scale",
                    value=10.0,
                    # on_change=self.on_ixamp,
                ).classes("w-full")
                self._iperiod = ui.select(
                    options=TSIZES,
                    label="Window size",
                    value=0.05,
                    on_change=self.on_iperiod,
                ).classes("w-full")
                self._istep = ui.select(
                    options=TSIZES,
                    label="Step size",
                    value=0.05,
                    # on_change=self.on_istep,
                ).classes("w-full")
                self._ichannel = ui.select(
                    options=[0],
                    label="Channel",
                    value=0,
                    # on_change=self.on_ichannel,
                ).classes("w-full")

            with ui.pyplot(figsize=(10, 5), close=False) as self.plot:
                self.ax = self.plot.fig.add_subplot()

    def adapt_interface(self):
        logger.debug("SpectrogramMode.adapt_interface()")
        if self.plot is None:
            logger.error("init_interface should be called before adapt_interface")
            return

        with self.plot:
            # Remove old line.
            if self.image is not None:
                self.ax.clear()
            # Set new parameters.
            if self.channel is None:
                logger.error("SpectrogramMode.adapt_interface: _channel is None")
                return

            image = np.zeros((self._nframes, 1, 3))

            self.image = self.ax.imshow(
                image.transpose(1, 0, 2),
                interpolation="none",
                aspect="auto",
                clim=(0, 1),
                origin="lower",
            )
            self.ax.set_xlabel("Time (sec)")
            self.ax.set_ylabel("Frequency (kHz)")
        ui.update(self.plot)

    def process_input(self, nsamples: int):
        if self.pointer is None:
            return
        self._samples_to_read += nsamples
        samples_per_frame = self.nsamples
        if samples_per_frame is None:
            logger.error("SpectrogramMode.process_input: samples_per_frame is None")
            return
        if self._samples_to_read < samples_per_frame:  # Not enough data.
            return
        skip = self.step_in_samples
        shift = (self._samples_to_read - samples_per_frame) // skip
        self.pointer.skip(shift * skip)
        self._samples_to_read -= shift * skip
        # logger.debug(f"SpectrogramMode.process_input: {nsamples=} {self._samples_to_read=} {samples_per_frame=} {skip=} {shift=}")
        data = self.pointer.extract(samples_per_frame)
        if data is None:  # End of stream
            return
        self.pointer.skip(skip)
        self._samples_to_read -= skip
        shift += 1

        # Compute spectrum of last frame.
        np_window = HannWindow().in_time_domain(nsamples=samples_per_frame)
        frame = PCMFrame(
            data=data, samplerate=self.pointer.stream.samplerate, np_window=np_window
        )
        spectrum = Spectrum.from_pcm(frame)
        # logger.debug(f"SpectrogramMode.on_timer: {shift} frames are read.")
        # Shift old frames.
        nframes = self.spectra.shape[0]
        if shift < nframes:
            self.spectra[: nframes - shift] = self.spectra[shift:]
        # Mark skipped frames.
        self.spectra[max(0, nframes - shift) : -1] = 0
        # Save spectrum of newest frame.
        amp = spectrum.camp
        nfreq = min(self.spectra.shape[1], amp.shape[0])
        self.spectra[-1, :nfreq] = amp[:nfreq]

    def redraw(self):
        if self.pointer is None:
            return
        if self.image is None:
            logger.error("BasicMode.adapt_interface was not called.")
            return

        image = camp_to_rgb(
            self.spectra[:, :, self.channel] / self.ampscale
        )  # Amplitude + phase
        # image = np.abs(self.spectra[:,:,self.channel]/self.ampscale)[:,:,None] # Amplitude only.
        with self.plot:
            self.image.set_data(image.transpose(1, 0, 2))
            self.image.set_extent([-self.memory_sec, 0, 0, self.maxfreq / 1e3])
            # self.image.set_clim(0, self.ampscale) # Disables plot updates.
        ui.update(self.plot)

    @property
    def channel(self):
        return self._ichannel.value

    @property
    def nsamples(self):
        return int(self.stream.samplerate * self._iperiod.value)

    @property
    def step_in_samples(self):
        return int(self.stream.samplerate * self._istep.value)

    @property
    def memory_sec(self):
        return self._istep.value * self._nframes

    @property
    def maxfreq(self):
        return self.stream.samplerate / 2

    @property
    def ampscale(self):
        return np.sqrt(self.nsamples) / self._ixamp.value

    def on_iperiod(self, msg):
        # logger.debug(f"SpectrogramMode.on_tscale({msg.value=})")
        self.create_spectra()
        # Update step.
        self._istep.value = max(t for t in self._istep.options.keys() if t <= msg.value)
        # ui.update(self._istep)
