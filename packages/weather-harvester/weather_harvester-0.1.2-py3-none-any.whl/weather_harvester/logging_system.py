import logging
from pathlib import Path

LOG_FILE = Path("data/app.log")

def setup_logging(level: str = "INFO", show_init_log: bool = True):
    """
    Initialize logging for the application.

    Parameters:
        level (str): Logging level ("DEBUG", "INFO", etc.)
        show_init_log (bool): Whether to print the initialization message.
    """
    LOG_FILE.parent.mkdir(exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

    if show_init_log:
        logging.info(f"Logging initialized with level: {level}")
