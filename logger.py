"""
Logger Class
"""
from functools import lru_cache
import logging
from config import get_settings

settings = get_settings()

"""
Following same signature as python logging (logging.getLogger)
"""


@lru_cache(maxsize=1)
def get_logger():
    """
    Get the logger
    """
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)-8s] %(message)s (%(filename)s:%(lineno)s)",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    log = logging.getLogger("copy-scenario")
    log.setLevel(settings.log_level.upper())
    return log
