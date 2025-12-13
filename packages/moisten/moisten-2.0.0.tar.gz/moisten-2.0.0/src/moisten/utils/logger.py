import logging
from rich.logging import RichHandler

logger = logging.getLogger("moisten")
logger.addHandler(RichHandler(log_time_format="[%y/%m/%d %X]",
                              keywords=['Moisten'], show_path=False))

logger.setLevel(logging.INFO)