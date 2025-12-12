from functools import wraps
from time import sleep
from crcmod.predefined import Crc
from ekfsm.log import ekfsm_logger

logger = ekfsm_logger(__name__)


def get_crc16_xmodem(data: bytes) -> int:
    crc16_xmodem = Crc("xmodem")
    crc16_xmodem.update(data)
    return crc16_xmodem.crcValue


def retry(max_attempts=5, delay=0.5):
    """
    Retry decorator.

    Decorator that retries a function a number of times before giving up.

    This is useful for functions that may fail due to transient errors.

    Note
    ----
    This is needed for certain PMBus commands that may fail due to transient errors
    because page switching timing is not effectively handled by older kernel versions.

    Important
    ---------
    This decorator is _not_ thread-safe across multiple ekfsm processes. Unfortunately,
    we cannot use fcntl or flock syscalls with files on virtual filesystems like sysfs.

    Parameters
    ----------
    max_attempts
        The maximum number of attempts before giving up.
    delay
        The delay in seconds between attempts.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.exception(
                            f"Failed to execute {func.__name__} after {max_attempts} attempts: {e}"
                        )
                        raise e
                    logger.info(f"Retrying execution of {func.__name__} in {delay}s...")
                sleep(delay)

        return wrapper

    return decorator
