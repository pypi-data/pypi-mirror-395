import logging

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

import logging
from IPython.display import display
import ipywidgets as widgets

# Créez un widget de sortie pour les logs
log_output = widgets.Output()
display(log_output)


# Configuration du logger
class OutputWidgetHandler(logging.Handler):
    def __init__(self, output_widget):
        super().__init__()
        self.output_widget = output_widget

    def emit(self, record):
        with self.output_widget:
            print(self.format(record))

def getlogger(_name, _level=logging.ERROR):
    """Get a logger with the specified name and level.

    Example:
        from keeshond.logging_logger import getlogger
        log = getlogger(__name__)
    """
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logger = logging.getLogger(_name)
    logger.setLevel(_level)
    if not logger.hasHandlers():
        handler = OutputWidgetHandler(log_output)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - "%(pathname)s:%(lineno)d" - %(funcName)s:  %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.info(f"{logger.name=} with level {logging.getLevelName(logger.getEffectiveLevel())} is enabled")
    return logger

