from functools import cached_property

import numpy as np

from .frame import PCMFrame
from .stream import CachedStream, PCMData, PCMStreamPointer, StreamPointer
from .window import RectangularWindow, Window

#################################################################################
# Sections/frames
#################################################################################


class PCMSections:
    def __init__(self, frames: list[PCMFrame] = None):
        if frames is None:
            frames = []
        self.frames = frames

    def __getitem__(self, index: int) -> PCMFrame:
        if index < 0:
            raise KeyError
        if index >= len(self.frames):
            return None
        return self.frames[index]

    def to_stream(self) -> "PCMSectionsStream":
        return PCMSectionsStream(self)

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @cached_property
    def nsections(self):
        """Return number of sections. Force to read stream upto the end."""
        return len(self.frames)


#################################################################################


class PCMSequenceSections(PCMSections):
    def __init__(self, memory: int = None):
        super().__init__(frames=[])
        self.memory = memory
        self.last_frame_start = None
        self.next_frame_index = 0

    @cached_property
    def nsections(self):
        """Return number of sections. Force to read stream upto the end."""
        n = self.last_frame_index
        while self[n] is not None:
            n += 1
        return n

    def _next(self) -> PCMFrame:
        """
        Obtain next frame. Should not be called directly.
        Frames can of arbitrary size, but beginning of the frames must go in increasing order.
        """
        raise NotImplementedError

    def next(self) -> PCMFrame:
        frame = self._next()
        if frame is None:
            return None

        assert isinstance(frame, PCMFrame)
        assert (
            self.last_frame_start is None or frame.first_sample >= self.last_frame_start
        )

        self.frames.insert(0, frame)
        self.frames = self.frames[: self.memory]
        self.last_frame_start = frame.first_sample
        self.next_frame_index += 1
        return frame

    def read_upto_position(self, position: int):
        while self.last_frame_start is None or self.last_frame_start < position:
            frame = self.next()
            if frame is None:
                break

    def read_upto_frame(self, index: int):
        for _ in range(self.next_frame_index, index + 1):
            frame = self.next()
            if frame is None:
                break

    def __getitem__(self, index: int) -> PCMFrame:
        self.read_upto_frame(index)  # Read missing frames.
        idx = self.next_frame_index - index - 1  # Index of the frame in the cache.
        if idx < 0:  # If the frame was not obtained, the end of the stream is reached.
            return None  # Signal end of stream.
        if idx > len(self.frames):
            raise IndexError(
                f"Frame index {index} is smaller than the last remembered frame {self.next_frame_index - 1}."
            )
        return self.frames[idx]


#################################################################################


class UniformPCMSections(PCMSequenceSections):
    def __init__(self, nsamples: int, skip: int, window: Window, memory: int = None):
        super().__init__(memory=memory)

        self.nsamples = nsamples
        self.skip = skip
        self.memory = memory

        assert isinstance(window, Window)
        assert self.skip > 0
        assert self.nsamples > 0

        self.np_window = window.in_time_domain(self.nsamples)


#################################################################################


class PCMStreamSections(UniformPCMSections):
    def __init__(
        self,
        ptr: PCMStreamPointer,
        nsamples: int,
        skip: int,
        window: Window,
        memory: int = None,
    ):
        super().__init__(nsamples=nsamples, skip=skip, window=window, memory=memory)

        self.pointer = ptr
        assert isinstance(self.pointer, StreamPointer)

    def _next(self) -> PCMFrame:
        frame = self.pointer.get_frame(nsamples=self.nsamples, np_window=self.np_window)
        self.pointer.skip(self.skip)
        return frame

    def close(self):
        self.pointer.detach()
        self.pointer = None


#################################################################################


class PCMLoudSections(PCMSequenceSections):
    def __init__(
        self,
        ptr: PCMStreamPointer,
        memory: int = None,
        window: Window = None,
        noise: float = 1,
        min_noise: float = 1e-5,
        min_silence: int = 1 << 10,
        estimation_halfdecay: int = 1 << 14,
        sound_trigger: float = 10,
        silence_trigger: float = 2,
        norm=2,
    ):
        super().__init__(memory=memory)

        assert isinstance(window, Window)
        assert noise > 0
        assert min_noise > 0
        assert estimation_halfdecay is None or estimation_halfdecay >= min_silence

        if silence_trigger is None:
            silence_trigger = sound_trigger

        assert sound_trigger >= silence_trigger >= 1

        self.norm = norm

        self._window = window
        self._silence_trigger = silence_trigger
        self._sound_trigger = sound_trigger

        self._size = min_silence
        self._sections = PCMStreamSections(
            ptr=ptr,
            nsamples=self._size,
            skip=self._size,
            window=RectangularWindow(),
            memory=1,
        )
        self._next_section = 0
        self._pulse = []

        self._estimation_sections = (
            estimation_halfdecay // self._size
            if estimation_halfdecay is not None
            else None
        )
        self._discount = (
            0.5 ** (1 / self._estimation_sections)
            if self._estimation_sections is not None
            else None
        )
        self._min_noise = min_noise
        self._noise = noise

    def _norm(self, data):
        if self.norm == 2:
            return np.sqrt(np.mean(data**2))
        elif np.isnan(self.norm):
            return np.max(np.abs(data))
        else:
            raise ValueError("Unknown norm")

    def _next(self) -> PCMFrame:
        # Always start from silence state.
        record = False
        run = True
        # Detect sound and record corresponding frames.
        blocks = []
        while run:
            frame = self._sections[self._next_section]
            if frame is None:
                break
            self._next_section += 1
            lvl = self._norm(frame.data)
            # State machine.
            if record:  # Inside sound region.
                if (
                    lvl < self._silence_trigger * self._noise
                ):  # Next silence interval is detected.
                    run = False
                    record = False
            else:  # Inside silence region.
                if (
                    lvl > self._sound_trigger * self._noise
                ):  # Sound segment is detected.
                    record = True
            # Remember the loud frames.
            if record:
                blocks.append(frame)
            # Update noise level.
            if self._discount is not None:
                self._noise = 1 / (
                    self._discount / self._noise
                    + (1 - self._discount) / (lvl + self._min_noise)
                )
        # If nothing is stored, then end of is stream is reached.
        if len(blocks) == 0:
            return None
        # Convert saved blocks to a frame and return.
        waveform = (
            PCMSections(frames=blocks)
            .to_stream()
            .new_pointer()
            .to_waveform(offset_t=blocks[0].t0)
        )
        return PCMFrame.from_waveform(waveform=waveform, window=self._window)

    def close(self):
        self._sections.close()

    @property
    def noise(self):
        return self._noise


#################################################################################
# Streams
#################################################################################


class PCMSectionsStream(PCMData, CachedStream):
    def __init__(self, sections: PCMSections, guard: float = 1e-16):
        super().__init__()
        self.sections = sections
        self.guard = guard
        assert isinstance(self.sections, PCMSections)
        self._read_zero_frame()

    @property
    def samplerate(self):
        return self._samplerate

    @property
    def nchannels(self):
        return self._nchannels

    def _remove_cache(self):
        self._last_stored_sample_position = None
        self._nvalid = 0
        self._data = None
        self._weight = None

    def _read_zero_frame(self):
        self.next_frame_index = 0
        frame = self.sections[self.next_frame_index]
        if frame is None:  # Empty sections.
            return self._remove_cache()
        # Remember the frame.
        self._last_stored_sample_position = 0
        self._nvalid = nsamples = frame.data.shape[0]
        self._data = frame.data.copy()
        self._weight = np.empty(nsamples)
        self._weight[:] = frame.np_window
        self.next_frame_index += 1
        # Update stream info
        self._samplerate = frame.samplerate
        self._nchannels = frame.nchannels

    def get_next_chunk(self) -> np.ndarray:
        frame = self.sections[self.next_frame_index]  # Get next frame.
        # print(f"get_next_chunk {frame is None=} {self._nvalid=} {self._last_stored_sample_position=} {self.next_frame_index=}")
        if frame is None:  # If no more frames are available,
            if self._data is None:  # If nothing is cached,
                return None  # signal end of stream.
            # Return cached data
            result = self._data[: self._nvalid] / (
                self._weight[: self._nvalid, None] + self.guard
            )  # Return stored data from earlier frames.
            self._remove_cache()
            return result
        # Append next frame.
        nsamples = frame.nsamples  # Frame length in samples.
        skip = min(
            frame.first_sample - self._last_stored_sample_position, self._nvalid
        )  # Length of the part that is not affected by other frames.
        noverlap = self._nvalid - skip
        # print(f"{nsamples=} {skip=} {noverlap=} {frame.first_sample=}")
        assert nsamples >= skip >= 0
        # Extract finished part for return.
        result = self._data[:skip] / (self._weight[:skip, None] + self.guard)
        # Expand cache if necessary.
        data, weight = self._data, self._weight

        # 1st variant: avoid memory allocation, but buggy.
        if data.shape[0] < nsamples:
            self._data = self._data.resize((nsamples,) + data.shape[1:])
            self._weight = self._weight.resize((nsamples,))
        # 2nd variant: reallocate memory for each frame.
        # self._data = np.empty((nsamples,)+data.shape[1:])
        # self._weight = np.empty((nsamples,))

        # Shift cached values and mix with new ones.
        self._data[:noverlap] = data[skip : self._nvalid] + frame.data[:noverlap]
        self._weight[:noverlap] = (
            weight[skip : self._nvalid] + frame.np_window[:noverlap]
        )
        # Save non overlapping part of new frame.
        self._data[noverlap:nsamples] = frame.data[noverlap:]
        self._weight[noverlap:nsamples] = frame.np_window[noverlap:]
        # Update state.
        self._last_stored_sample_position = frame.first_sample
        self._nvalid = nsamples
        self.next_frame_index += 1
        # print(f"end {self._last_stored_sample_position=} {self._nvalid=} {self.next_frame_index=} {self._data.shape}")
        return result
