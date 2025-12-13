from nicegui import ui
from time import perf_counter
import soundfile as sf

from ..io.stream import AbstractStream, SoundDeviceStream, SoundFileStream
from ..ngui import local_file_picker
from .log import logger

##################################################################################
# Classes implementing signal sources.


class Source:
    NAME = "Abstract"

    def __init__(self, on_select=None, on_deselect=None):
        self._on_select = on_select
        self._on_deselect = on_deselect

    def init_interface(self, timer):
        pass

    @property
    def stream(self) -> AbstractStream:
        raise NotImplementedError

    def activate(self):
        logger.debug("Source.activate()")

    def deactivate(self):
        logger.debug("Source.deactivate()")

    def get_position_in_samples(self) -> int:
        raise NotImplementedError

    def announce_natural_step(self, step_in_sec: float):
        """
        The method is called from Mode to notify about time step while selecting position in signal in file-like sources.
        """
        pass


##################################################################################


class DummySource(Source):
    NAME = "Dummy"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def stream(self) -> AbstractStream:
        return None

    def init_interface(self):
        logger.debug("DummySource.init_interface()")
        with ui.row().classes("w-full"):
            ui.label("Dummy input")

    def get_position_in_samples(self) -> int:
        return 0


##################################################################################


class DeviceSource(Source):
    NAME = "Device"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._devices = self.list_audio_devices()
        self._source = None

    def list_audio_devices(self):
        logger.debug("DeviceSource.list_audio_devices()")
        devices = SoundDeviceStream.input_devices()
        devices[-1] = "Select input device to start"
        return devices

    def _release_device(self):
        if self._source is None:
            return
        self._source.stop()
        self._source.close()
        self._source = None

    def on_device_select(self, msg):
        logger.debug(f"DeviceSource.on_device_select({msg.value}=)")
        if self._on_deselect is not None:
            self._on_deselect()
        # Close previous device if necessary.
        self._release_device()
        # Get selected device id.
        device = msg.value
        # Create new device connection.
        if device >= 0:
            try:
                self._source = SoundDeviceStream(device=device)
            except Exception as e:
                logger.error(f"Failed to open input: {e}")
                ui.notify("Device is not available")
                return
            self._source.start()
            logger.debug(
                f"Device {device}: {self._source.samplerate} samples/sec {self._source.nchannels} channels"
            )
        else:
            logger.debug("Disconnected from sound device.")
        if self._on_select is not None:
            self._on_select()

    def activate(self):
        logger.debug("DeviceSource.activate()")
        super().activate()
        if self._source is not None:
            self._source.start()

    def deactivate(self):
        logger.debug("DeviceSource.deactivate()")
        if self._source is not None:
            self._source.stop()
        super().deactivate()

    @property
    def stream(self) -> AbstractStream:
        return self._source

    def init_interface(self):
        logger.debug("DeviceSource.init_interface()")
        with ui.row().classes("w-full"):
            ui.select(
                self._devices,
                label="Input device",
                on_change=self.on_device_select,
                value=-1,
            )

    def get_position_in_samples(self) -> int:
        if self._source is None:
            return None
        return self._source.get_last_available_sample()


##################################################################################


class FileSource(Source):
    NAME = "File"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._file: sf.SoundFile = None
        self._source = None
        self._position = None
        self._last_update = None

    def init_source(self, position: int = None):
        # If initialized without position set.
        if position is None:
            # open stream and forget old position.
            self._source = SoundFileStream(file=self._file)
            self._position = None
            self._last_update = None
            return
        # Check if file seekable.
        if not self._file.seekable():
            ui.notify("File is not seekable")
            return
        self._file.seek(position)
        self._source = SoundFileStream(file=self._file)
        self._position = position
        self._last_update = None

    def on_file_select(self, filename):
        logger.debug(f"FileSource.on_file_select({filename})")
        # Emit deselect event.
        if self._on_deselect is not None:
            self._on_deselect()
        # Close previous file if necessary.
        if self._file is not None:
            self._file.close()
        self._source = None
        self._file = None
        # If file is specified.
        if filename is None:
            logger.debug("File is closed.")
        else:
            # Open stream.
            try:
                self._file = sf.SoundFile(file=filename, mode="r")
                self.init_source()
            except Exception as e:
                logger.error(f"Failed to open input: {e}")
                ui.notify("Device is not available")
                return
            # Debug info.
            logger.debug(
                f"File {filename}: {self._source.samplerate} samples/sec {self._source.nchannels} channels"
            )
            # Update UI.
            self._islider._props["max"] = (
                self._source.get_length_in_samples() / self._source.samplerate
            )
            self._islider.update()
        # Emit select event.
        if self._on_select is not None:
            self._on_select()

    def activate(self):
        logger.debug("FileSource.activate()")
        super().activate()

    def deactivate(self):
        logger.debug("FileSource.deactivate()")
        super().deactivate()

    @property
    def stream(self) -> AbstractStream:
        return self._source

    async def pick_file(self) -> None:
        result = await local_file_picker(".", multiple=False)
        if result is None or len(result) != 1:
            ui.notify("Nothing is selected")
            self.on_file_select(None)
        else:
            filename = result[0]
            ui.notify(f"Open file {filename}.")
            self.on_file_select(filename)

    def init_interface(self):
        logger.debug("FileSource.init_interface()")

        SPEED = {
            0.1: "x1/10",
            0.25: "x1/4",
            0.5: "x1/2",
            1: "x1",
            2: "x2",
            10: "x10",
        }

        # with ui.row().classes("w-full items-center"):
        with ui.row().classes("w-full items-center"):
            ui.button(text="Open", on_click=self.pick_file, icon="folder").classes(
                "w-1/12"
            )

            self._iplay = ui.switch(text="Play", value=True)

            self._ispeed = ui.select(SPEED, label="Speed", value=1).classes("w-1/12")

            self._inumber = ui.number(
                label="Time",
                value=0.0,
                format="%.3f",
                on_change=self.on_change_position,
            ).classes("w-1/12")

            self._islider = (
                ui.slider(
                    min=0,
                    max=1,
                    step=0.1,
                    value=0,
                )
                .bind_value(self._inumber)
                .classes("w-5/12")
            )

    def set_position(self, position_in_sec: float):
        if self._file is None:
            return
        # Check if position is actually different from the current one, i.e. selected by user.
        position = int(position_in_sec * self._file.samplerate)
        if self._position is None or abs(self._position - position) < 10:
            # Position is already correct. Exiting.
            return
        logger.debug(
            f"FileSource.set_position({position_in_sec}): {self._position} -> {position}"
        )
        # Emit deselect event.
        if self._on_deselect is not None:
            self._on_deselect()
        # Get target position in samples.
        self.init_source(position)
        # Emit select event.
        if self._on_select is not None:
            self._on_select()

    def on_change_position(self, msg):
        self.set_position(position_in_sec=msg.value)

    def get_position_in_samples(self) -> int:
        # Return None if no file is open.
        if self._source is None:
            return
        # On the first access set initial values to the current ones.
        current_time = perf_counter()
        if self._last_update is None:
            self._last_update = current_time
        if self._position is None:
            self._position = 0
        # Compute time increment and update position accordingly.
        delta = (
            0
            if not self._iplay.value
            else int(
                (current_time - self._last_update)
                * self._source.samplerate
                * self.speed
            )
        )
        self._position += delta
        self._last_update = current_time
        # Update UI.
        if delta > 0:
            self._inumber.value = self._position / self._source.samplerate
        return self._position

    @property
    def speed(self):
        return self._ispeed.value

    @property
    def play(self):
        return self._iplay.value

    def announce_natural_step(self, step_in_sec: float):
        logger.debug(f"FileSource.announce_natural_step({step_in_sec=})")
        self._islider._props["step"] = step_in_sec
        self._islider.update()
        self._inumber._props["step"] = step_in_sec
        self._inumber.update()
