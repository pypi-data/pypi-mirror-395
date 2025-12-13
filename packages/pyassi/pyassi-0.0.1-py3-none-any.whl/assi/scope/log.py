import logging

from nicegui import ui

##################################################################################
# Logger

logger = logging.getLogger("assi-scope")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

##################################################################################
# Graphic logger


class LogElementHandler(logging.Handler):
    """A logging handler that emits messages to a log element."""

    def __init__(self, element: ui.log, level: int = logging.NOTSET) -> None:
        self.element = element
        super().__init__(level)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.element.push(msg)
        except Exception:
            self.handleError(record)


def place_log():
    global logger
    log = ui.log(max_lines=64).classes("w-full")
    handler = LogElementHandler(log)
    logger.addHandler(handler)
    # logger.setLevel(logging.DEBUG)
    ui.context.client.on_disconnect(lambda: logger.removeHandler(handler))
