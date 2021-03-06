# coding=utf-8

import logging.config
import requests
from flask import Flask, request, json, send_file, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime as dt
import datetime
from fact_extraction.run import extract_facts
from fact_extraction.network_utils import (
    success_response,
    error_response,
    requires_auth,
    STATUSES,
)
from create_ical import create_event, create_ical, save_ical
import json as js
app = Flask(__name__)
CORS(app)
logger = logging.getLogger(__name__)

REALTY_ALL_FIELDS = [
    "to-do list",
    "купить",
    "продать",
    "встреча"
]

predef_messages = [
    "Привет, к завтрашнему дню надо чтобы ты подготовил презентацию и выложил в папку и скинул ссылку в общий чат. После стэндапа сделаем тестовый прогон.",
    "Привет, кончилась еда, нужно купить молоко и сыр, пельмени и сметану",
    "Привет, назначь встречу с Марком Цукербергом на 20-07-2018 19:00",
    "Привет, назначь встречу с Марком Цукербергом на 2 августа на 10:00"
]


@app.route('/message/<id>', methods=['GET'])
def ping(id):
    if int(id) <4:
        return success_response(predef_messages[int(id)])
    else:
        params = {'access_token': '57da9ea5824071cab4da378434ba71d9ba735fb537363830',
                  'email':'smartmail_team11@mail.ru',
                  'only_html':'false',
                  'mark_read':'true',
                  'id':id}
        resp = requests.post("https://e.mail.ru/api/v1/messages/message", params).json()
        return success_response(resp['body']['body']['text'])


@app.route('/get_ical', methods=['POST'])
def get_ical():
    content = js.loads(request.form['mm'])
    print(content)
    logger.info('Extracting all realty facts from message %s', content)
    facts = extract_facts(content['message'])['facts']
    logger.info('Extracted facts %s', facts)
    events = []
    fname = "cal"
    for fact in facts:

        if fact['date']:
            date = fact['date'][0].split('-')
        else:
            date = datetime.date.today() + datetime.timedelta(days=1)
            date = [date.day, date.month, date.year]

        if fact['time']:
            time = fact['time'].split('-')
        else:
            time = [10,0]

        fname = fact['action']
        if fact['checklist']:
            checklist = " \n ".join(fact['checklist'])
        else:
            checklist = fact['action']
        print(date, time, checklist)
        events.append(create_event(dt(int(date[2]),int(date[1]),int(date[0]),int(time[0]),int(time[1]),0), fact['action'], checklist))
        save_ical(events, 'cal')

    return send_from_directory("","cal.ics")
