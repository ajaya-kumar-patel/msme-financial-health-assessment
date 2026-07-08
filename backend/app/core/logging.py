import logging
import sys

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level=logging.INFO):
    """
    Configure application-wide logging.

    Call once when the FastAPI application starts.
    """

    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        stream=sys.stdout,
        force=True,          # overwrite uvicorn default logging
    )


def get_logger(name: str):
    """
    Return a logger instance.
    """

    return logging.getLogger(name)