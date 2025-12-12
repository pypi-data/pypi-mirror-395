import inspect

from keeshond import logging_logger
from keeshond.format_dict import format_dict

log = logging_logger.getlogger(__name__, logging_logger.DEBUG)


def analyze(_object):
    # Get the current frame
    locals_dict = inspect.currentframe().f_back.f_locals
    for key, value in locals_dict.items():
        if isinstance(value, dict):
            log.debug(f"{key}={format_dict(value)}")
        else:
            log.debug(f"{key}={value!r}")
    log.debug(f"{type(_object)=}")
    log.debug(f"{dir(_object)=}")
    try:
        log.debug(f"{_object.__dict__=}")
    except Exception as e:
        log.warning(f"_object.__dict__ {e=}")
    try:
        log.debug(f"{vars(_object)=}")
    except Exception as e:
        log.warning(f"vars(_object) {e=}")
    log.debug(f"{help(_object)=}")
    try:
        log.debug(f"{inspect.getargvalues(_object)=}")
    except Exception as e:
        log.warning(f"inspect.getargvalues(_object) {e=}")
        pass
    log.debug(f"{inspect.getmembers(_object)=}")
