import logging
import typing

import colorlog


def configure_logging(verbose: int, log_file: str | None = None) -> None:
    """Configure logging for both import and gen-data scripts."""
    # Define TRACE level
    logging.TRACE = 5  # type: ignore[attr-defined]
    logging.addLevelName(logging.TRACE, "TRACE")  # type: ignore[attr-defined]

    def trace(
        self: logging.Logger,
        message: object,
        *args: typing.Any,  # noqa: ANN401
        **kws: typing.Any,  # noqa: ANN401
    ) -> None:
        if self.isEnabledFor(logging.TRACE):  # type: ignore[attr-defined]
            self._log(logging.TRACE, message, args, **kws)  # type: ignore[attr-defined]

    logging.Logger.trace = trace  # type: ignore[attr-defined]

    # Get root logger
    root = logging.getLogger()

    # Define formatter for file logging.
    fmt = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")

    # Define formatter for colored console logging.
    color_fmt = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s %(levelname)-8s %(message)s",
        log_colors={
            "TRACE": "light_cyan",
            "DEBUG": "light_yellow",
            "INFO": "light_green",
            "WARNING": "light_purple",
            "ERROR": "light_red",
            "CRITICAL": "light_red",
        },
    )

    # Define console handler
    color_handler = colorlog.StreamHandler()
    color_handler.setFormatter(color_fmt)
    root.addHandler(color_handler)

    # Set log file
    if log_file is not None:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(fmt)
        root.addHandler(fh)

    level_map = {
        0: logging.WARNING,  # quiet mode
        1: logging.INFO,  # default
        2: logging.DEBUG,  # verbose mode
    }
    level = level_map.get(verbose)
    # If verbose is greater than 2, set level to TRACE.
    root.setLevel(level if level else logging.TRACE)  # type: ignore[attr-defined]
