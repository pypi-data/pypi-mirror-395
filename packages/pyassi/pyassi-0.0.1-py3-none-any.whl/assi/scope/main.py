from time import perf_counter

from nicegui import ui

from .beamformer import Beamformer1Mode
from .log import logger
from .mode import DummyMode, Mode, OscilloscopeMode, SpectrogramMode, SpectrumMode
from .source import DeviceSource, DummySource, FileSource, Source

##################################################################################
# Auxiliary functions


def pair_source_and_mode(source: Source, mode: Mode, timer):
    logger.debug(f"pair_source_and_mode({source=}, {mode=}, {timer=})")
    if source is None or mode is None:
        return
    mode.attach(source)
    mode.adapt_interface()
    source.activate()
    timer.active = True


def unpair_source_and_mode(source: Source, mode: Mode, timer):
    timer.active = False
    if source is None or mode is None:
        return
    source.deactivate()
    mode.detach()


##################################################################################
# Pages.

SOURCES = [FileSource, DeviceSource, DummySource]
MODES = [OscilloscopeMode, SpectrumMode, SpectrogramMode, Beamformer1Mode, DummyMode]


@ui.page("/")
def scope_page() -> None:
    current_mode: Mode = None
    current_source: Source = None
    framerate = 10

    # Schedule updates.
    last_redraw = None
    last_position = None
    samples_read = 0

    def on_timer():
        nonlocal timer, current_mode, last_redraw, last_position, samples_read
        # Do nothing is no mode selected.
        if (
            current_mode is None
            or current_source is None
            or current_source.stream is None
        ):
            return
        # Stop timer.
        timer.active = False
        # Compute how many samples to read.
        current_position = current_source.get_position_in_samples()
        if last_position is None:
            last_position = current_position
        nsamples = current_position - last_position
        nsamples = max(nsamples, current_mode.nsamples_to_prebuffer - samples_read)
        last_position = current_position
        # logger.debug(f"scope_page on_timer {nsamples=} {delta_time=}")

        # Process input
        current_mode.process_input(nsamples)
        samples_read += nsamples
        # Update graphics, but limit framerate.
        current_time = perf_counter()
        if last_redraw is None:
            last_redraw = current_time
        progress = (current_time - last_redraw) * framerate

        if progress >= 1:
            last_redraw = current_time
            # logger.debug("scope_page on_timer: redraw")
            current_mode.redraw()
        # Enable further processing.
        timer.active = True

    # Timer interval should be much smaller than 1/framerate.
    timer = ui.timer(interval=0.001, callback=on_timer, once=False, active=False)

    def do_unpair():
        nonlocal current_mode, current_source, timer, last_redraw, last_position
        unpair_source_and_mode(mode=current_mode, source=current_source, timer=timer)

    def do_pair():
        nonlocal \
            current_mode, \
            current_source, \
            timer, \
            last_redraw, \
            last_position, \
            samples_read
        last_redraw = None
        last_position = None
        samples_read = 0
        pair_source_and_mode(mode=current_mode, source=current_source, timer=timer)

    modes = {f"{n}": cls() for n, cls in enumerate(MODES)}
    inputs = {
        f"{n}": cls(on_select=do_pair, on_deselect=do_unpair)
        for n, cls in enumerate(SOURCES)
    }

    def on_input_select(msg):
        nonlocal current_source
        logger.debug(f"on_input_select {msg.value=}")
        do_unpair()
        current_source = inputs[msg.value]
        do_pair()

    def on_mode_select(msg):
        nonlocal current_mode
        logger.debug(f"on_mode_select {msg.value=}")
        do_unpair()
        current_mode = modes[msg.value]
        do_pair()

    # Input selection.
    with ui.row().classes("w-full"):
        input_selector = ui.select(
            {n: inp.NAME for n, inp in inputs.items()},
            label="Input",
            on_change=on_input_select,
            value="0",
        ).classes("w-1/12")
        # sel = ui.toggle({f"{n}": inp.NAME for n, inp in enumerate(inputs)}, value='0')
        with ui.carousel().props("height=70px").classes("py-0 w-10/12") as carousel:
            for n, inp in inputs.items():
                with ui.carousel_slide(name=n).classes("p-0 w-full"):
                    inp.init_interface()
        carousel.bind_value(input_selector, "value")
    current_source = inputs[
        input_selector.value
    ]  # For some reason on_input_select is not called with initial value.
    # ui.separator()

    # Oscilloscope mode.
    mode_tabs = {}
    with ui.tabs(on_change=on_mode_select) as tabs:
        for n, m in modes.items():
            mode_tabs[n] = ui.tab(n, label=m.NAME)
    with ui.tab_panels(tabs, value="0", animated=False).classes("w-full"):
        for n, m in modes.items():
            with ui.tab_panel(mode_tabs[n]):
                m.init_interface()

    # with ui.expansion('Log output', icon='log').classes('w-full'):
    #     place_log()
    logger.debug("scope_page: loaded")
