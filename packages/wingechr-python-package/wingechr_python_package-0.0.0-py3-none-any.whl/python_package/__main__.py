import logging

import click

try:  # optional module
    import coloredlogs
except ModuleNotFoundError:
    coloredlogs = None

from typing import Literal

from . import __version__


def setup_logging(
    level: Literal[
        "DEBUG", "INFO", "WARNING", "ERROR", "d", "i", "w", "e", 10, 20, 30, 40
    ] = "WARNING",
    name: str = None,
    logfile: str = None,
    fmt: str = "[%(asctime)s %(levelname)7s] %(message)s",
    datefmt: str = "%Y-%m-%d %H:%M:%S",
) -> None:
    logger = logging.getLogger(name)

    # assert at least one streaming handler
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())

    # add file handler
    if logfile:
        logger.addHandler(
            logging.FileHandler(filename=logfile, mode="a", encoding="utf-8")
        )

    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    # set level (logger and handlers)
    if isinstance(level, str):
        level = level[0].upper()
        level = {"D": "DEBUG", "I": "INFO", "W": "WARNING", "E": "ERROR"}[level]
        level = getattr(logging, level)

    logger.setLevel(level)
    for h in logger.handlers:
        h.setLevel(level)
        h.setFormatter(formatter)

    if coloredlogs:
        coloredlogs.DEFAULT_LOG_FORMAT = fmt
        coloredlogs.DEFAULT_DATE_FORMAT = datefmt
        coloredlogs.DEFAULT_FIELD_STYLES = {
            "asctime": {"color": "white"},
            "levelname": {"color": "white"},
        }
        coloredlogs.DEFAULT_LEVEL_STYLES = {
            "debug": {"color": "blue"},
            "info": {"color": "green"},
            "warning": {"color": "yellow"},
            "error": {"color": "red"},
        }
        coloredlogs.install(level=level)


@click.command()  # or @click.group()
@click.pass_context
@click.version_option(__version__)
@click.option(
    "--loglevel",
    "-l",
    type=click.Choice(["debug", "info", "warning", "error"], case_sensitive=False),
    default="info",
    show_default=True,
)
def main(ctx, loglevel):
    """Script entry point."""
    ctx.ensure_object(dict)  # create special ctx.obj
    setup_logging(level=loglevel)


if __name__ == "__main__":
    main(prog_name=None)
