import logging
import os

from rich.logging import RichHandler

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
def init_logger():
    # Configure logging
    if DEBUG:   
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[RichHandler(rich_tracebacks=True)]
        )
    else:
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[RichHandler(rich_tracebacks=True)]
        )
