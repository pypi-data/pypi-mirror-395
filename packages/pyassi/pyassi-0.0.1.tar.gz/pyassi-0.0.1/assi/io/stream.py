import queue
import sys
from typing import Iterator, Optional

import numpy as np
import soundfile as sf

from .frame import PCMFrame, Waveform

# import typing


# from .window import Window

#################################################################################
# Pointers
#################################################################################


class StreamPointer:
    def __init__(self, stream: "AbstractStream", position: int = 0):
        """
        Create pointer to the `stream`, pointing to the `position`.
        """
        self._position = position
        self._stream = stream
        assert isinstance(self._stream, AbstractStream)

    # Properties.
    @property
    def position(self) -> int:
        return self._position

    @property
    def stream(self) -> "AbstractStream":
        return self._stream

    # Main functions.
    def skip(self, nsamples: int):
        """
        Advance given `nsamples` in the stream.
        """
        assert nsamples >= 0
        self._position += nsamples
        self._stream.drop_unused()

    def extract(self, nsamples: int) -> Optional[np.ndarray]:
        """
        Return data frame of length no longer than `nsamples` from the associated stream
        or None if end of stream is reached.
        """
        return self._stream.extract(position=self._position, nsamples=nsamples)

    # More pointers.
    def duplicate(self) -> "StreamPointer":
        return self._stream.new_pointer(position=self.position)

    # Free resources.
    def detach(self):
        self._stream._remove_pointer(self)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.detach()

    def is_ready(self, nsamples: int) -> bool:
        """
        Check if given number of samples can be returned by `StreamPointer.extract` without blocking.
        """
        return self._stream.is_ready(self._position, nsamples)


#################################################################################


class PCMStreamPointer(StreamPointer):
    def __init__(self, stream: "AbstractStream", position: int = 0):
        super().__init__(stream=stream, position=position)

    def get_frame(self, nsamples: int, np_window: np.ndarray) -> PCMFrame:
        data = self.extract(nsamples=nsamples)
        if data is None:
            return None
        if (
            data.shape[0] < nsamples
        ):  # Drop incomplete chunk, since window can not be applied.
            return None
        data = (
            data * np_window[:, None]
        )  # Avoid inplace operation. Buffer should not be changed.
        return PCMFrame(
            data=data,
            samplerate=self._stream.samplerate,
            first_sample=self._position,
            np_window=np_window,
        )

    def to_waveform(
        self, nsamples: int = None, chunk_size: int = 1 << 14, offset_t: float = 0
    ):
        position = self.position
        chunks = []
        while nsamples is None or nsamples > 0:
            chunk = self.extract(
                nsamples=chunk_size if nsamples is None else min(chunk_size, nsamples)
            )
            if chunk is None:
                break
            sz = chunk.shape[0]
            self.skip(sz)
            if nsamples is not None:
                nsamples -= sz
            chunks.append(chunk)
        data = np.concatenate(chunks, axis=0)
        samplerate = self.stream.samplerate
        return Waveform(
            data=data, samplerate=samplerate, t0=offset_t + position / samplerate
        )


#################################################################################
# Streams
#################################################################################


class PCMData:
    def _new_pointer(self, position: int = 0) -> PCMStreamPointer:
        return PCMStreamPointer(stream=self, position=position)


#################################################################################


class AbstractStream:
    def __init__(self):
        self._pointers = []

    # Properties
    @property
    def samplerate(self):
        raise NotImplementedError

    @property
    def nchannels(self):
        raise NotImplementedError

    @property
    def first_available_sample(self) -> int:
        raise NotImplementedError

    @property
    def pointers(self) -> Iterator[StreamPointer]:
        return iter(self._pointers)

    # Access to stream.
    def _remember_pointer(self, pointer: StreamPointer):
        assert pointer.position >= self.first_available_sample
        self._pointers.append(pointer)
        return pointer

    def new_pointer(self, position: int = None) -> StreamPointer:
        if position is None:
            position = self.first_available_sample
        return self._remember_pointer(self._new_pointer(position=position))

    # Low level interface.
    def drop_unused(self):
        position = min(ptr.position for ptr in self._pointers)
        self._drop_before_position(position)

    def _remove_pointer(self, pointer: StreamPointer):
        self._pointers.remove(pointer)

    # Abstract methods.
    def extract(self, position: int, nsamples: int) -> np.ndarray:
        """
        Return samples from `position` of length `nsamples`.
        If necessary, read uncached data from the source.
        Raise ValueError if `position>self.first_available_sample`.
        """
        raise NotImplementedError

    def is_ready(self, position: int, nsamples: int) -> bool:
        """
        Check if call to `extract` with given parameters will not block.
        The result of the call of `extract` does not matter, it can be None.
        Default implementation always returns True.
        """
        return True

    def _drop_before_position(self, position: int):
        """
        Remove all the data from cache upto `position`.
        Should not be called directly.
        """
        raise NotImplementedError

    # Helpers.
    def time(self, position: int, nsamples: int) -> np.ndarray:
        return np.arange(position, position + nsamples) / self.samplerate


#################################################################################


class ArrayStream(AbstractStream):
    def __init__(self, array: np.ndarray, samplerate: int):
        super().__init__()
        self._samplerate = samplerate
        self._array = array
        assert isinstance(self._array, np.ndarray)
        assert self._array.ndim == 2

    @property
    def samplerate(self):
        return self._samplerate

    @property
    def nchannels(self):
        return self._array.shape[1]

    @property
    def nsamples(self):
        return self._array.shape[0]

    @property
    def first_available_sample(self) -> int:
        return 0

    def extract(self, position: int, nsamples: int) -> np.ndarray:
        if position >= self.nsamples:
            return None
        return self._array[position : position + nsamples]

    def _drop_before_position(self, position: int):
        pass


#################################################################################


class WaveformStream(PCMData, ArrayStream):
    def __init__(self, waveform: Waveform):
        assert isinstance(waveform, Waveform)
        ArrayStream.__init__(self, array=waveform.data, samplerate=waveform.samplerate)


#################################################################################


class CachedStream(AbstractStream):
    def __init__(self):
        super().__init__()
        self._cached_data = []
        self._read_samples = 0
        self._first_available_sample = 0

    # Abstract methods
    def get_next_chunk(self) -> np.ndarray:
        raise NotImplementedError

    def is_next_chunk_ready(self) -> bool:
        return True

    # Information on stream.
    def _count_read_chunks(self):
        return sum(c.shape[0] for c in self._cached_data)

    # Caching implementation.
    def _read_chunk(self):
        chunk = self.get_next_chunk()
        if chunk is None:
            return False
        self._cached_data.append(chunk)
        self._read_samples += chunk.shape[0]
        return True

    def precache_upto(self, position: int):
        """
        Read chunks until sample at `position` is cached.
        """
        # print(f"precache_upto({position=})")
        # Read chunks until necessary number of samples is read or end of stream is reached.
        while self._first_available_sample + self._read_samples < position:
            if not self._read_chunk():
                break

    # Implementation of the interface functions.
    @property
    def first_available_sample(self) -> int:
        return self._first_available_sample

    def extract(self, position: int, nsamples: int) -> np.ndarray:
        # print(f"extract({position=}, {nsamples=}) {self._first_available_sample=}")

        assert position >= 0 and nsamples > 0
        # Precache.
        self.precache_upto(position + nsamples)
        # Set position relative to the first cached sample.
        position -= self._first_available_sample
        assert position >= 0
        # Find relevant chunks.
        blocks = []
        for chunk in self._cached_data:
            # print(f"   {position=}, {nsamples=}, {len(blocks)=}")
            if nsamples <= 0:
                break
            datal = chunk.shape[0]  # Chunk length in samples.
            if position >= datal:  # If read position is after the chunk,
                position -= datal  # skip it.
                continue
            if position > 0:
                chunk = chunk[
                    position:
                ]  # Drop part of the chunk that was not requested.
                position = 0  # No more skip.
                datal = chunk.shape[0]  # Update length of available data.
            if datal <= nsamples:  # The required number of samples is not reached.
                blocks.append(chunk)
                nsamples -= datal
            else:  # Excess data.
                blocks.append(chunk[:nsamples])
                nsamples = 0  # Stop reading.
        # print(f"   {position=}, {nsamples=}, {len(blocks)=}")
        # If nothing is read, signal end of file.
        if len(blocks) == 0:
            return None
        # Merge chunks.
        result = np.concatenate(blocks, axis=0)
        return result

    def is_ready(self, position: int, nsamples: int) -> bool:
        """
        Check if given number of samples can be read from the given position without blocking.
        Read data from the stream until required position is reached or next chunk is not available.
        """
        while self._first_available_sample + self._read_samples <= position + nsamples:
            if not self.is_next_chunk_ready():
                return False
            if not self._read_chunk():
                break
        return True

    def _drop_before_position(self, position: int):
        while len(self._cached_data) > 0 and position > self._first_available_sample:
            chunk = self._cached_data.pop(0)
            datal = chunk.shape[0]  # Chunk length in samples.
            nsamples = (
                position - self._first_available_sample
            )  # Number of samples to abandon.
            if datal <= nsamples:  # The required number of samples is not reached.
                nsamples -= datal
                self._read_samples -= datal
                self._first_available_sample += datal
            else:  # Excess data.
                self._cached_data.insert(0, chunk[nsamples:])  # Return some data.
                self._read_samples -= nsamples
                self._first_available_sample += nsamples
                nsamples = 0

    def get_last_available_sample(self) -> int:
        while self.is_next_chunk_ready():
            if not self._read_chunk():
                break
        return self._first_available_sample + self._read_samples


#################################################################################
# Simulated streams.
#################################################################################


class FunctionStream(AbstractStream):
    def __init__(self, samplerate: int, nsamples: int, function):
        super().__init__()
        self._samplerate = samplerate
        self._nsamples = nsamples
        self.function = function
        test = self.function(self.time(position=0, nsamples=2))
        self._nchannels = test.shape[1]

    @property
    def samplerate(self):
        return self._samplerate

    @property
    def nchannels(self):
        return self._nchannels

    @property
    def nsamples(self):
        return self._nsamples

    @property
    def first_available_sample(self) -> int:
        return 0

    # @typing.override
    def extract(self, position: int, nsamples: int) -> np.ndarray:
        if position >= self.nsamples:
            return None
        t = self.time(
            position=position, nsamples=min(nsamples, self.nsamples - position)
        )
        return self.function(t)

    # @typing.override
    def _drop_before_position(self, position: int):
        pass


#################################################################################
# File input.
#################################################################################


class SoundFileStream(PCMData, CachedStream):
    def __init__(self, file, chunk_size=1 << 14):
        super().__init__()
        self.chunk_size = chunk_size
        if isinstance(file, str):
            self.file = sf.SoundFile(file=file, mode="r")
        elif isinstance(file, sf.SoundFile):
            self.file = file
        else:
            raise ValueError(f"Unsupported file object {file}.")

    # Properties.
    @property
    def samplerate(self):
        return self.file.samplerate

    @property
    def nchannels(self):
        return self.file.channels

    # Show available resources.
    @staticmethod
    def show_available_formats():
        print("Available formats:")
        formats = sf.available_formats()
        for format, desc in formats.items():
            print(f"{format}: {desc}")

    # Context manager.
    def __enter__(self):
        # print(f"Input stream {self.file.name}, {self.file.samplerate} hz, {self.file.channels} ch.")
        self.file.__enter__()
        return self

    def __exit__(self, *vargs):
        # print(f"Close input stream {self.file.name}.")
        self.file.__exit__(*vargs)

    def close(self):
        self.file.close()

    # Abstract methods
    # @typing.override
    def get_next_chunk(self) -> np.ndarray:
        chunk = self.file.read(frames=self.chunk_size, always_2d=True)
        return None if chunk.shape[0] == 0 else chunk

    def get_length_in_samples(self):
        return self.file.frames


#################################################################################
# Device input.
#################################################################################


class SoundDeviceStream(PCMData, CachedStream):
    def __init__(
        self, device: int = None, samplerate: int = None, nchannels: int = None
    ):
        import sounddevice as sd

        super().__init__()
        self.device_id = device

        self.nlost = 0

        self.queue = queue.Queue()
        self._stream = sd.InputStream(
            samplerate=samplerate,
            device=self.device_id,
            channels=nchannels,
            dtype=None,
            latency=None,
            callback=self.process_input,
        )
        self._stream.start()

    # Properties
    @property
    def samplerate(self):
        return self._stream.samplerate

    @property
    def nchannels(self):
        return self._stream.channels

    # Inspect hardware.
    @staticmethod
    def input_devices() -> dict[int, str]:
        import sounddevice as sd

        result = {}
        devices = sd.query_devices()
        for device in devices:
            ch = device["max_input_channels"]
            if ch <= 0:
                continue
            result[device["index"]] = (
                f"{device['name']}: [{device['default_samplerate']} hz {ch} ch]"
            )
        return result

    # Context manager.
    def __enter__(self):
        # print(f"Input device # {self._stream.device}, {self._stream.samplerate} hz, {self._stream.channels} ch.")
        self.start()

    def __exit__(self, *_vargs):
        # print(f"Close input device # {self._stream.device}.")
        self.stop()

    def start(self):
        self._stream.start()

    def stop(self):
        self._stream.abort()
        # self._stream.stop()

    def close(self):
        self._stream.close()

    # Save new data.
    def process_input(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        try:
            self.queue.put_nowait(indata.copy())
        except queue.Full:
            self.nlost += 1

    # Abstract methods
    # @typing.override
    def get_next_chunk(self) -> np.ndarray:
        data = self.queue.get()
        return data

    # @typing.override
    def is_next_chunk_ready(self) -> bool:
        return not self.queue.empty()


#################################################################################
# Output stream.
#################################################################################


class PCMSink:
    @property
    def samplerate(self) -> int:
        raise NotImplementedError

    @property
    def nchannels(self) -> int:
        raise NotImplementedError

    def write(self, data):
        raise NotImplementedError


#################################################################################
# File output.
#################################################################################


class PCMFileSink(PCMSink):
    def __init__(self, filename, samplerate: int, nchannels: int, format: str = "FLAC"):
        self.file = sf.SoundFile(
            file=filename,
            mode="w",
            samplerate=samplerate,
            channels=nchannels,
            format=format,
            subtype=None,
        )

    # Properties.
    @property
    def samplerate(self) -> int:
        return self.file.samplerate

    @property
    def nchannels(self) -> int:
        return self.file.channels

    # Context manager.
    def __enter__(self):
        print(
            f"Output stream {self.file.name}, {self.file.samplerate} hz, {self.file.channels} ch."
        )
        return self.file.__enter__()

    def __exit__(self, *vargs):
        print(f"Close output stream {self.file.name}.")
        self.file.__exit__(*vargs)

    # Save data.
    def write(self, data):
        self.file.write(data)


#################################################################################
# Device output.
#################################################################################

# class PCMDeviceSink(PCMSink):
#     def __init__(self, device:int=None, samplerate:int=48000, nchannels:int=None):
#         super().__init__()
#         self.device = device
#         self.samplerate = samplerate
#         self.nchannels = nchannels

#         self.queue = queue.Queue()
#         self._stream = sd.OutputStream(samplerate=samplerate,
#             device=self.device,
#             channels=self.nchannels,
#             dtype=None,
#             latency=None,
#             callback=self.process_output,
#             )

#     # Inspect hardware.
#     @staticmethod
#     def show_output_devices():
#         print("Available input devices:")
#         devices = sd.query_devices()
#         for device in devices:
#             ch = device['max_output_channels']
#             if ch<=0: continue
#             print(f"{device['index']}: `{device['name']}` {device['default_samplerate']} hz {ch} ch")

#     # Context manager.
#     def __enter__(self):
#         print(f"Output device # {self._stream.device}, {self._stream.samplerate} hz, {self._stream.channels} ch.")
#         return self._stream.__enter__()

#     def __exit__(self, *vargs):
#         print(f"Close output device # {self._stream.device}.")
#         self._stream.__exit__(*vargs)

#     # Save new data.
#     def process_output(self, outdata: np.ndarray, frames:int, time, status):
#         """This is called (from a separate thread) for each audio block."""
#         if status:
#             print(status, file=sys.stderr)
#         data = self.queue.get()
#         outdata[:] = data # Size mismatch. Should be cached in advance.

#     # Save data.
#     def write(self, data):
#         self.queue.pu(data)
