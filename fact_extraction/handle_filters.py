# coding=utf-8

import logging
import re

from string import punctuation
from datetime import datetime

logger = logging.getLogger(__name__)


def normalize_all_params(raw_parameters):
    facts = {'facts': [{}]}
    if all([x is None for x in raw_parameters['type']]):
        facts['facts'][0]['checklist'] = None
    else:
        facts['facts'][0]['checklist'] = raw_parameters['type']

    if all([x is None for x in raw_parameters['action']]):
        facts['facts'][0]['action'] = None
    else:
        facts['facts'][0]['action'] = raw_parameters['action']

    if raw_parameters['TimeFact'][0] == None:
        facts['facts'][0]['time'] = None
    else:
        facts['facts'][0]['time'] = '-'.join(['%02d'%i if i is not None else '00' for i in raw_parameters['TimeFact']])

    if raw_parameters['DateFact'][4] is not None:
        facts['facts'][0]['date'] = raw_parameters['DateFact'][4]
        return facts
    if raw_parameters['DateFact'][3] is not None:
        pass
    if all([x is None for x in raw_parameters['DateFact'][0:3]]):
        facts['facts'][0]['date'] = None
        return facts
    elif raw_parameters['DateFact'][2] is None:
        raw_parameters['DateFact'][2] = datetime.now().year

    facts['facts'][0]['date'] = '-'.join(['%02d'%i for i in raw_parameters['DateFact'][0:3]])
    return facts



if __name__ == '__main__':
    print(normalize_all_params({
    'DateFact': [28, 7, None, None, None],
    'TimeFact': [None, None],
    'CheckListFact': [None, None],
    'ActionFact': [None],
}))
