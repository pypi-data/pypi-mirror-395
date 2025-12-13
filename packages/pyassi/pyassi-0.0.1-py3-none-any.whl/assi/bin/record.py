import typer
import soundfile as sf
import sounddevice as sd

# import numpy as np
# import time
import queue
import sys
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
import rich
from datetime import datetime


app = typer.Typer()

q = queue.Queue()


def process_input(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())


@app.command()
def record(
    device: int = None,
    output: str = None,
    samplerate: int = 48000,
    channels: int = None,
    format: str = "FLAC",
):
    if output is None:
        output = f"{datetime.now():%y%m%d_%H%M%S}.flac"
    with sd.InputStream(
        samplerate=samplerate,
        device=device,
        channels=channels,
        dtype=None,
        latency=None,
        callback=process_input,
    ) as stream:
        rich.print(
            f"Input device # [yellow]{stream.device}[/], {stream.samplerate} hz, {stream.channels} ch."
        )
        with sf.SoundFile(
            file=output,
            mode="w",
            samplerate=int(stream.samplerate),
            channels=stream.channels,
            format=format,
            subtype=None,
        ) as file:
            rich.print(f"Writing to [yellow]`{file.name}`[/]")
            with Progress(
                SpinnerColumn(),
                TimeElapsedColumn(),
            ) as progress:
                print("Press Ctrl-C to stop recording.")
                task1 = progress.add_task("[red]Recording", total=None)
                try:
                    while True:
                        progress.update(task1)
                        file.write(q.get())
                except KeyboardInterrupt:
                    print("Stop recording.")


@app.command()
def inputs():
    print("Available input devices:")
    devices = sd.query_devices()
    for device in devices:
        ch = device["max_input_channels"]
        if ch <= 0:
            continue
        print(
            f"{device['index']}: `{device['name']}` {device['default_samplerate']} hz {ch} ch"
        )


@app.command()
def formats():
    print("Available formats:")
    formats = sf.available_formats()
    for format, desc in formats.items():
        print(f"{format}: {desc}")


def main():
    app()
