import os
import sys
import io
import logging
from datetime import datetime
import structlog


class CustomLogger:
    def __init__(self, log_dir="logs"):
        # Ensure logs directory exists
        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)

        # Timestamped log file (for persistence)
        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        self.log_file_path = os.path.join(self.logs_dir, log_file)

    def get_logger(self, name=__file__):
        logger_name = os.path.basename(name)

        # FILE HANDLER: force UTF-8 so symbols are saved correctly
        file_handler = logging.FileHandler(self.log_file_path, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))  # Raw JSON lines

        # CONSOLE HANDLER: try to use UTF-8 for output as well
        console_stream = io.TextIOWrapper(
            sys.stdout.buffer,
            encoding="utf-8",
            errors="replace",  # avoid crashing if console can't display a char
        )
        console_handler = logging.StreamHandler(stream=console_stream)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",  # Structlog will handle JSON rendering
            handlers=[console_handler, file_handler],
            force=True,  # overwrite previous basicConfig if something else set it
        )

        # Configure structlog for JSON structured logging (no ASCII escaping)
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer(ensure_ascii=False),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger(logger_name)
