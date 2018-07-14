# coding=utf-8
import logging.config

from settings import LOGGING_DICT

from views import app



if __name__ == '__main__':
    logging.config.dictConfig(LOGGING_DICT)
    logger = logging.getLogger(__name__)

    app.run(host='0.0.0.0', port=80, debug=False)
