import json
import sys

from loguru import logger

from bitpulse.core.settings import app_settings


def setup_logging():
    logger.remove()
    env = str(app_settings.env).lower()

    def json_sink(message):
        record = message.record

        data = {
            "time": record["time"].strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "level": record["level"].name,
            "file": record["file"].path,
            "line": record["line"],
            "function": record["function"],
            "message": record["message"],
        }

        sys.stdout.write(json.dumps(data) + "\n")

    if env == "production":
        logger.add(
            json_sink,
            level=app_settings.log_level,
            backtrace=False,
            diagnose=False,
            enqueue=True,
        )
    else:
        human_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level}</level> | "
            "<cyan>{file}</cyan>:<cyan>{line}</cyan> "
            "<magenta>{function}</magenta> - "
            "<level>{message}</level>"
        )
        logger.add(
            sys.stdout,
            format=human_format,
            level=app_settings.log_level,
            backtrace=False,
            diagnose=False,
        )

    return logger
