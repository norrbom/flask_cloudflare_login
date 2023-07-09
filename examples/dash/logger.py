from os import getenv
import logging
import logging.config


def configure_logging():
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "default": {
                    "format": "%(asctime)s.%(msecs)03d [%(process)d] [%(levelname)s] %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "default_app": {
                    "format": "%(asctime)s.%(msecs)03d [%(process)d] [%(levelname)s] [%(filename)s] %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
                "stdout_app": {
                    "class": "logging.StreamHandler",
                    "formatter": "default_app",
                },
            },
            "loggers": {
                "gunicorn": {"propagate": False, "handlers": ["stdout"]},
                "gunicorn.access": {"propagate": False, "handlers": ["stdout"]},
                "gunicorn.error": {"propagate": False, "handlers": ["stdout"]},
                "flask_cloudflare_login.access": {
                    "propagate": True,
                },
                getenv("APP_NAME"): {
                    "propagate": True,
                    "level": getenv("LOG_LEVEL", "INFO"),
                },
            },
            "root": {
                "handlers": ["stdout_app"],
                "level": getenv("LOG_LEVEL", "INFO"),
            },
        }
    )
