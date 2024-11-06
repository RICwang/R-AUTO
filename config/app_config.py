# config.py
import logging

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s',
        },
    },
    'handlers': {
        'fileHandler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'volume/logs/logger-app.log',
            'maxBytes': 20 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'default',
            'encoding': 'utf-8',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['fileHandler']
    }
}