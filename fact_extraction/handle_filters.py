# coding=utf-8

import logging
import re

from string import punctuation
from datetime import datetime

logger = logging.getLogger(__name__)


def normalize_all_params(raw_parameters):
    facts = {'facts': [{}]}
    print(raw_parameters)
    if not raw_parameters.get('type'):
        facts['facts'][0]['checklist'] = None
    else:
        facts['facts'][0]['checklist'] = [chl.lower() for chl in raw_parameters['type']]

    if not raw_parameters.get('action'):
        facts['facts'][0]['action'] = None
    else:
        facts['facts'][0]['action'] = raw_parameters['action'][0].lower()

    if not raw_parameters.get('Hour'):
        facts['facts'][0]['time'] = None
    else:
        time = raw_parameters.get('Minutes') if raw_parameters.get('Minutes') else 0
        print([int(i[0]) for i in [raw_parameters.get('Hour'), time]])
        facts['facts'][0]['time'] = '-'.join(['%02d'%int(i[0]) for i in [raw_parameters.get('Hour'), time]])

    if raw_parameters.get('Full'):
        facts['facts'][0]['date'] = raw_parameters.get('Full')
        return facts
    if raw_parameters.get('DayOfWeek'):
        pass
    day = raw_parameters.get('Day')
    month = raw_parameters.get('Month')
    year = raw_parameters.get('Year')
    if not any([day, month, year]):
        facts['facts'][0]['date'] = None
        return facts
    elif not year:
        year = [str(datetime.now().year)]
        print(year)
    facts['facts'][0]['date'] = ['-'.join(['%02d'%int(i[0]) for i in [day, month, year]])]
    return facts



if __name__ == '__main__':
    print(normalize_all_params({
        'Day':[28],
        'Month':[7],
        'Year':None,
        'DayOfWeek':None,
        'Full':None,
        'Hour':None,
        'Minutes':None,
        'type':None,
        'action':None
    }))
