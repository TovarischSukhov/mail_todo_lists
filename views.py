# coding=utf-8

import logging.config

from flask import Flask, request, json

from fact_extraction.run import extract_facts
from fact_extraction.network_utils import (
    success_response,
    error_response,
    requires_auth,
    STATUSES,
)

app = Flask(__name__)
logger = logging.getLogger(__name__)

REALTY_ALL_FIELDS = [
    "balcony",
    "toilet",
    "ipoteka",
    "places",
    "possible_places",
    "price",
    "rooms",
    "size",
    "undefined_readable",
]


@app.route('/ping', methods=['GET'])
def ping():
    return success_response('YAY!')


@app.route('/get_ical/', methods=['POST'])
@requires_auth
def get_realty_facts_all():
    message = request.args.get('message')
    if not message:
        logger.info('No message passed in request.')
        return error_response('It is required to pass message', STATUSES['HTTP_400_bad_request'])
    logger.info('Extracting all realty facts from message %s', message)
    facts = {"facts": {key: val for key, val in extract_facts(message).items() if key in REALTY_ALL_FIELDS}}
    logger.info('Extracted facts %s', facts)
    return success_response(facts)
