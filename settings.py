import os

LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': 'logs/common.log',
            'mode': 'a',
            'formatter': 'standard',
            'maxBytes': 10240000,
            'backupCount': 3,
            'encoding': 'utf8'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'propagate': True
        },
    }
}
