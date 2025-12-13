import sys
import numpy as np
from nicegui import ui
import glob
from pathlib import Path

from ..io.frame import PCMFrame, Spectrum

# from ..io.stream import AbstractStream, PCMStreamPointer
# from ..io.util import camp_to_rgb
from ..io.window import HannWindow
from .log import logger

# from .source import Source
from .mode import BasicMode

##################################################################################
# Aux functions.


def gaussian(x, mean, std, normalize=True):
    y = np.exp(-((x - mean) ** 2) / (2 * std**2))
    if normalize:
        y = y / np.sqrt(np.sum(y**2))
    return y


##################################################################################
# Plugins for BeamformerMode.


class Beamformer1Plugin:
    NAME = "Beamformer1Plugin"

    def __init__(self, parent: BasicMode):
        assert isinstance(parent, Beamformer1Mode)
        self._parent = parent
        self._steering = None
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

    def init_colors(self, nfreq: int):
        x = np.linspace(0, 1, nfreq)
        self._torgb = np.stack(
            (
                gaussian(x, mean=0.25, std=0.2),
                gaussian(x, mean=0.5, std=0.2),
                gaussian(x, mean=0.75, std=0.2),
            ),
            axis=0,
        )  # (color, freq)

    def compute_colors(self, amp: np.ndarray) -> np.ndarray:
        # amp (freq,angle)
        rgb = np.einsum("fa,cf->ac", amp, self._torgb)  # (angle,color)
        return rgb


##################################################################################


class BasicBeamformer1Plugin(Beamformer1Plugin):
    NAME = "Basic"

    def adapt(self, spectrum):
        # Clear
        self._parent.ax.clear()
        # Precompute constants.

        # Set new parameters.
        yscale = self._parent._iyscale.value
        ax = self._parent.ax
        ax.set_ylim(0, yscale)
        ax.set_xlim(self._angles[0], self._angles[-1])
        rgb = self.process(spectrum)
        COLOR = ["r", "g", "b"]
        self._lines = list(
            self._parent.ax.plot(
                self._angles, rgb[:, c], ls="-", color=COLOR[c], lw=0.2
            )[0]
            for c in range(3)
        )
        ax.set_xlabel("Angle of incidence (rad)")
        ax.set_ylabel("Amplitude")
        ax.set_yscale("linear")

    def redraw(self, spectrum):
        rgb = self.process(spectrum)
        for c, line in enumerate(self._lines):
            line.set_data(self._angles, rgb[:, c])

    def process(self, spectrum) -> np.ndarray:
        # spectrum (freq)
        scale = 2 * spectrum.shape[0]
        spectrum = spectrum / scale
        chances = np.abs(
            np.einsum("fc,fac->fa", spectrum, self._steering)
        )  # (freq,angle)
        rgb = self.compute_colors(chances)
        # logger.debug(f"{np.max(np.abs(spectrum))=}")
        return rgb

    def on_yscale(self, scale: float):
        ax = self._parent.ax
        if ax is not None:
            ax.set_ylim(0, scale)

    def configure(
        self, micarray: np.ndarray, gridsize: int, freqs: np.ndarray, speed: float
    ):
        self.init_colors(nfreq=freqs.shape[0])
        self._angles = np.linspace(-np.pi, np.pi, gridsize)  # (angle) [rad]
        dx, dy = np.cos(self._angles), np.sin(self._angles)  # (angle) [m]
        delay = (
            micarray[None, :, 0] * dx[:, None] + micarray[None, :, 1] * dy[:, None]
        ) / speed  # (angle, sensor) [sec]
        ratio = freqs[:, None, None] * delay[None]  # (freq,angle,sensor) [1]
        self._steering = np.exp(2j * np.pi * ratio)  # (freq,angle,sensor)


##################################################################################
# Beamformer interface


class BeamformerMode(BasicMode):
    NAME = "Abstract Beamformer"
    PLUGINS = None

    def __init__(self, cfg_folder="cfg/micarray/"):
        super().__init__()
        self._spectrum = None
        self._plugin: Beamformer1Plugin = None
        self._time_in_samples = 0
        self._cfg_folder = cfg_folder
        self._micarray_locs = None

    def list_micarrays(self) -> list[str]:
        names = glob.glob(f"./{self._cfg_folder}/*.csv")
        rules = {ord("_"): ord(" ")}
        # rules = {}
        result = {n: Path(n).stem.translate(rules) for n in names}
        if len(names) == 0:
            logger.error(
                "No microphone array config files found. Be sure folder 'cfg/micarray' is available in the current directory."
            )
            sys.exit(1)
        logger.debug(
            f"Beamformer.list_micarray: Folder {self._cfg_folder} contains config files {(*result.values(),)}"
        )
        return result

    def parse_micarray(self, name) -> np.ndarray:
        locs = np.loadtxt(f"{name}")
        logger.debug(
            f"Beamformer.micarray: config {name}, locations shape {locs.shape}."
        )
        if locs.shape[1] != 3:
            raise ValueError("Microphone positions should be defined in 3d space.")
        return locs

    def adapt_interface(self):
        logger.debug("BeamformerMode.adapt_interface()")
        if self.plot is None:
            logger.error("init_interface should be called before adapt_interface")
            return
        if self.pointer is None:  # Not connected to input.
            return
        self.on_configure()

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

    def redraw(self):
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
        logger.debug("BeamformerMode.init_ui_left_column()")
        super().init_ui_left_column()

        micarrays = self.list_micarrays()
        self._imicarray = ui.select(
            options=micarrays,
            value=next(iter(micarrays.keys())),
            label="Microphone array",
            on_change=self.on_micarray_select,
        ).classes("w-full")

        names = list(p.NAME for p in self.PLUGINS)
        self._iplugin = ui.select(
            options=names,
            on_change=self.on_plugin_select,
            value=names[0],
            label="Beamformer type",
        ).classes("w-full")

        self._ispeed = ui.number(
            label="Speed of sound (m/s)",
            value=343,
            min=290,
            max=460,
            step=1,
            precision=0,
            on_change=self.on_configure,
        ).classes("w-full")

        self.on_plugin_select()
        self.on_micarray_select()

    def on_plugin_select(self, msg=None):
        logger.debug(
            f"BeamformerMode.on_plugin_select({'' if msg is None else msg.value})"
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

    def on_micarray_select(self, msg=None):
        logger.debug(
            f"BeamformerMode.on_micarray_select({'' if msg is None else msg.value})"
        )
        value = self._imicarray.value if msg is None else msg.value
        self._micarray_locs = self.parse_micarray(value)
        self.on_configure()

    @property
    def speed_of_sound(self):
        return self._ispeed.value

    def on_configure(self, msg=None):
        logger.debug(f"BeamformerMode.on_configure({'' if msg is None else msg.value})")


##################################################################################
# 1d Beamformer interface


class Beamformer1Mode(BeamformerMode):
    NAME = "Beamformer 1D"
    PLUGINS = [
        BasicBeamformer1Plugin,
    ]

    def __init__(
        self,
    ):
        super().__init__()
        self._gridsize = 100

    def on_configure(self, msg=None):
        logger.debug(
            f"Beamformer1Mode.on_configure({'' if msg is None else msg.value})"
        )
        if self._plugin is None or self.stream is None:
            return
        nsamples = self.nsamples
        nfreq = nsamples // 2 + 1 if nsamples % 2 == 0 else (nsamples + 1) // 2
        samplerate = self.stream.samplerate
        freqs = np.linspace(0, samplerate, nfreq)  # (freq) [1/s]
        self._plugin.configure(
            micarray=self._micarray_locs,
            gridsize=self._gridsize,
            freqs=freqs,
            speed=self.speed_of_sound,
        )


##################################################################################
# Beamformer interface

# class Beamformer2Mode(BasicMode):
#     NAME = "Beamformer 2D"
#     PLUGINS = [BasicBeamformer2Plugin, ]

#     def __init__(self, cfg_folder='cfg/micarray/'):
#         super().__init__()
#         self._spectrum = None
#         self._plugin: Beamformer1Plugin = None
#         self._time_in_samples = 0
#         self._cfg_folder = cfg_folder
#         self._micarray_locs = None
#         self._gridsize = 100
#         self._gridcenter = None

#     def list_micarrays(self) -> list[str]:
#         names = glob.glob(f"./{self._cfg_folder}/*.csv")
#         rules = {ord('_'):ord(' ')}
#         # rules = {}
#         result = {n:Path(n).stem.translate(rules) for n in names }
#         logger.debug(f"Beamformer.list_micarray: Folder {self._cfg_folder} contains config files {*result.values(),}")
#         return result

#     def parse_micarray(self, name) -> np.ndarray:
#         locs = np.loadtxt(f"{name}")
#         logger.debug(f"Beamformer.micarray: config {name}, locations shape {locs.shape}.")
#         if locs.shape[1]!=3:
#             raise ValueError("Microphone positions should be defined in 3d space.")
#         return locs


#     def adapt_interface(self):
#         logger.debug("BeamformerMode.adapt_interface()")
#         if self.plot is None:
#             logger.error("init_interface should be called before adapt_interface")
#             return
#         if self.pointer is None:  # Not connected to input.
#             return
#         self.on_init_data()

#         nchannels = self.stream.nchannels
#         nsamples = self.nsamples
#         nfreq = nsamples//2+1 if nsamples%2==0 else (nsamples+1)//2

#         self._spectrum = np.zeros((nfreq, nchannels))
#         if self._plugin is not None:
#             with self.plot:
#                 self._plugin.adapt(self._spectrum)

#         ui.update(self.plot)

#     def attach(self, source):
#         super().attach(source)
#         self._time_in_samples = 0

#     def process_input(self, nsamples: int):
#         samples_per_frame=self.nsamples
#         data = self._receive_frame(nsamples=nsamples, samples_per_frame=samples_per_frame, skip=self.nsamples)
#         if data is None:
#             return
#         self._time_in_samples += data.shape[0]

#         # Save data.
#         np_window = HannWindow().in_time_domain(nsamples=samples_per_frame)
#         frame = PCMFrame(data=data, samplerate=self.pointer.stream.samplerate, np_window=np_window)
#         self._spectrum = Spectrum.from_pcm(frame).camp


#     def redraw(self):
#         if self.pointer is None or self._spectrum is None:
#             return

#         if self._plugin is not None:
#             with self.plot:
#                 self._plugin.redraw(self._spectrum)
#         ui.update(self.plot)

#     def on_yscale(self, msg):
#         scale = msg.value
#         if self._plugin is not None:
#             self._plugin.on_yscale(scale)

#     def init_figure(self):
#         with ui.pyplot(figsize=(7, 7), close=False) as self.plot:
#             self.ax = self.plot.fig.add_subplot()

#     def init_ui_left_column(self):
#         logger.debug("BeamformerMode.init_ui_left_column()")
#         super().init_ui_left_column()

#         micarrays = self.list_micarrays()
#         self._imicarray = ui.select(
#             options=micarrays,
#             value=next(iter(micarrays.keys())),
#             label='Microphone array',
#             on_change=self.on_micarray_select,
#         ).classes('w-full')

#         names = list(p.NAME for p in self.PLUGINS)
#         self._iplugin = ui.select(
#             options=names,
#             on_change=self.on_plugin_select,
#             value=names[0],
#             label='Beamformer type',
#             ).classes('w-full')

#         self._iradius = ui.number(
#             label = 'Domain size (m)',
#             value = 1,
#             min = 0.1,
#             max = 10,
#             step = 0.1,
#             precision = 2,
#             on_change=self.on_init_data,
#         ).classes('w-full')

#         self._ispeed = ui.number(
#             label = 'Speed of sound (m/s)',
#             value = 343,
#             min = 390,
#             max = 460,
#             step = 1,
#             precision = 0,
#             on_change=self.on_init_data,
#         ).classes('w-full')

#         self.on_plugin_select()
#         self.on_micarray_select()

#     def on_plugin_select(self, msg=None):
#         logger.debug(f"BeamformerMode.on_plugin_select({'' if msg is None else msg.value})")
#         name = self._iplugin.value
#         plugin = None
#         # Find plugin.
#         for p in self.PLUGINS:
#             if name==p.NAME:
#                 plugin = p
#                 break
#         # If unknown name.
#         if plugin is None:
#             logger.error(f"Unknown plugin name: {name}")
#             return
#         # Deinitialize previous plugin.
#         if self._plugin is not None:
#             self._plugin.stop()
#         # Create new plugin.
#         self._plugin = plugin(self)
#         # Prepare UI.
#         self.adapt_interface()

#     def on_micarray_select(self, msg=None):
#         logger.debug(f"BeamformerMode.on_micarray_select({'' if msg is None else msg.value})")
#         value = self._imicarray.value if msg is None else msg.value
#         self._micarray_locs = self.parse_micarray(value)
#         self._gridcenter = np.mean(self._micarray_locs, axis=0)

#     @property
#     def radius(self):
#         return self._iradius.value

#     @property
#     def speed_of_sound(self):
#         return self._ispeed.value

#     def on_init_data(self, msg=None):
#         logger.debug(f"BeamformerMode.on_init_data({'' if msg is None else msg.value})")
#         radius = self.radius
#         sz = self._gridsize
#         center = self._gridcenter
#         self._grid = np.stack(np.meshgrid(
#             np.linspace(center[0]-radius/2, center[0]+radius/2, sz),
#             np.linspace(center[1]-radius/2, center[1]+radius/2, sz),
#             [center[2]],
#             indexing='ij',
#         ), axis=0)
#         self._distance = np.sqrt(np.sum((self._grid[:,None]-self._micarray_locs.T[:,:,None,None,None])**2,axis=0)) # (sensor,x,y,z) [m]
#         nsamples = self.nsamples
#         nfreq = nsamples//2+1 if nsamples%2==0 else (nsamples+1)//2
#         samplerate = self.stream.samplerate
#         freqs = np.linspace(0, samplerate, nfreq) # (freq) [1/s]
#         self._phase = np.exp(2j*np.pi*freqs[:,None,None,None,None]/self.sp*self._distance[None]) # (freq,sensor,x,y,z)
#         self._torgb = np.stack(
#             (
#                 self._gaussian(freqs, mean=samplerate*0.25, std=0.2),
#                 self._gaussian(freqs, mean=samplerate*0.5, std=0.2),
#                 self._gaussian(freqs, mean=samplerate*0.75, std=0.2),
#             ), axis = 0
#         ) # (color, freq)

#     def compute_colors(self, spectrum:np.ndarray) -> np.ndarray:
#         # spectrum (freq)
#         amp = np.abs(np.einsum('f,fsxyz->fxyz',spectrum, self._phase)) # (freq,x,y,z)
#         mamp = np.max(amp, axis=3) # (freq,x,y)
#         rgb = np.einsum('fxy,cf->xyc',mamp,self._torgb) # (x,y,color)
#         return rgb
