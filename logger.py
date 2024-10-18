import logging
import os


def configure_logging():
    """
    Configures logging based on environment variables.
    """

    log_level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    log_level = log_levels.get(log_level_str, logging.INFO)

    log_file = os.getenv('LOG_FILE', 'app.log')
    log_to_file = os.getenv('LOG_TO_FILE', 'true').lower() == 'true'
    log_to_console = os.getenv('LOG_TO_CONSOLE', 'true').lower() == 'true'

    handlers = []
    if log_to_file:
        handlers.append(logging.FileHandler(log_file, "w", encoding="utf-8"))

    if log_to_console:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(module)s#%(lineno)d - %(levelname)s - %(message)s",
        handlers=handlers,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    return logging.getLogger(__name__)
