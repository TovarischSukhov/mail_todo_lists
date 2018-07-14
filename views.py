# coding=utf-8

import logging.config
from datetime import datetime
from flask import Flask, request, json, send_file

from fact_extraction.run import extract_facts
from fact_extraction.network_utils import (
    success_response,
    error_response,
    requires_auth,
    STATUSES,
)
from create_ical import create_event, create_ical

app = Flask(__name__)
logger = logging.getLogger(__name__)

REALTY_ALL_FIELDS = [
    "to-do list",
    "купить",
    "продать",
    "встреча"
]


@app.route('/ping', methods=['GET'])
def ping():
    return success_response('YAY!')


@app.route('/get_ical/', methods=['POST'])
@requires_auth
def get_ical():
    message = request.args.get('message')
    if not message:
        logger.info('No message passed in request.')
        return error_response('It is required to pass message', STATUSES['HTTP_400_bad_request'])
    logger.info('Extracting all realty facts from message %s', message)
    facts = {"facts": {key: val for key, val in extract_facts(message).items() if key in REALTY_ALL_FIELDS}}
    logger.info('Extracted facts %s', facts)
    events = []
    for fact in facts:

        if fact['date']:
            date = fact['date'].split('-')
        else:
            date = datetime.date.today() + datetime.timedelta(days=1)

        if fact['time']:
            time = fact['time'].split(':')
            events.append(create_event(datetime(int(date[2]),int(date[1]),int(date[0]),int(time[0]),int(time[1]),0), fact['action'], fact['checklist'].join("\n")))

    return send_file(create_ical(events))
