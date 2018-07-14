# coding=utf-8
import logging.config
import os

from fact_extraction.setup_parser import TomitaRunner
from settings import LOGGING_DICT

from views import app



if __name__ == '__main__':
    logging.config.dictConfig(LOGGING_DICT)
    logger = logging.getLogger(__name__)
    logger.info('Setup parser')

    parser = TomitaRunner(compile_dk=True)
    parser.setup()
    logger.info('Parser ready to go!')

    app.run(host='0.0.0.0', port=80, debug=False)
