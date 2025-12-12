import logging
from rich.logging import RichHandler


def config_log(level: int = logging.INFO):
    logging.basicConfig(level=level, handlers=[RichHandler(rich_tracebacks=True)])
