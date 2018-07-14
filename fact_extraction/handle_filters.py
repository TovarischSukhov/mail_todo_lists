# coding=utf-8

import logging
import re
import os
import pandas as pd

from string import punctuation

from settings import STOPWORDS

logger = logging.getLogger(__name__)

DATA_DIR = '/opt/project/data/'
STREETS = pd.concat([pd.read_csv(DATA_DIR + f) for f in os.listdir(DATA_DIR)])
STREETS['formal_by_word'] = STREETS.formalname.str.split(' ')

DIGIT = re.compile('\d[\d| |\.]*')

LETTER_SUMMS = {
    'миллион': 1000000,
    'тысяча': 1000,
}


def get_type(raw_parameters):
    return raw_parameters.get('type', [])


def normalize_rooms(raw_parameters):
    raw_rooms = raw_parameters.get('num_rooms', [])
    rooms = []
    for rm in raw_rooms:
        rooms.extend([r for r in rm if r.isdigit()])
        if rm.lower() == 'студия':
            rooms.append('st')
    return rooms


def get_figure(price, multiplier=None):
    if not price:
        return 0
    price = price[0].replace(',', '.')
    price_sum = [float(''.join(d.split(' '))) for d in re.findall(DIGIT, price)]
    if not multiplier:
        multiplier = []
    res = []
    if len(price_sum) == len(multiplier):
        for i, _ in enumerate(price_sum):
            res.append(int(price_sum[i] * LETTER_SUMMS[multiplier[i].lower()]))
    else:
        if multiplier:
            for i, _ in enumerate(price_sum):
                res.append(int(price_sum[i] * LETTER_SUMMS[multiplier[0].lower()]))
        else:
            for i, _ in enumerate(price_sum):
                res.append(int(price_sum[i]))
    if len(res) == 1:
        res = res[0]
    return res


def get_mulipliers(price):
    if not price:
        return []
    price = price[0]
    return [p for p in price.split(' ') if p.lower() in LETTER_SUMMS]


def normalize_price(raw_parameters):
    raw_price = raw_parameters.get('price', [])
    raw_price_min = raw_parameters.get('price_min', [])
    raw_price_max = raw_parameters.get('price_max', [])
    raw_price_about = raw_parameters.get('price_about', [])
    if raw_price_min or raw_price_max:
        mult_min = get_mulipliers(raw_price_min)
        mult_max = get_mulipliers(raw_price_max)
        if int(len(mult_min) == 0) ^ int(len(mult_max) == 0):
            price_min = get_figure(raw_price_min, mult_min + mult_max)
            price_max = get_figure(raw_price_max, mult_min + mult_max)
        elif int(len(mult_min)) > 0 and int(len(mult_max) > 0):
            price_min = get_figure(raw_price_min, mult_min)
            price_max = get_figure(raw_price_max, mult_max)
        elif int(len(mult_min) == 0) and int(len(mult_max) == 0):
            price_min = get_figure(raw_price_min)
            price_max = get_figure(raw_price_max)
        return {'price_min': price_min, 'price_max': price_max}
    elif raw_price_about:
        return {'price_about': get_figure(raw_price_about, get_mulipliers(raw_price_about))}

    elif raw_price:
        return {'price_unspecified': get_figure(raw_price, get_mulipliers(raw_price))}
    else:
        return


def normalize_place(raw_parameters):
    raw_place = raw_parameters.get('place', [])
    place_list = []
    if raw_place:
        for place in raw_place:
            place_list.append({"location": ' '.join([p for p in place.split(' ') if p.lower() not in STOPWORDS])})
    return place_list


def normalize_size(raw_parameters):
    raw_size = raw_parameters.get('total_size', [])
    size_list = []
    for size in raw_size:
        size_list.extend([int(i) for i in re.findall('\d+', size)])
    if len(size_list) == 1:
        return {"total": size_list[0]}
    elif len(size_list):
        return {"multiple": size_list}
    return {}


def get_undefined(raw_parameters):
    return [raw_parameters.get('undefined', '')]


def normalize_undefined(undefined):
    return ' '.join(
                [''.join(
                    [sym for sym in text if sym not in punctuation]
                ) for text in ' '.join(undefined).split(' ') if text not in STOPWORDS
                ]
            ).strip()


def get_possible_places(raw_parameters):
    possible_places = raw_parameters.get('possible_places', [])
    return [{"location": place} for place in possible_places]


def normalize_toilet(raw_parameters):
    divided = len(raw_parameters.get('divided', '')) > 0
    combined = len(raw_parameters.get('combined', '')) > 0
    toilet = {}
    if any([divided, combined]):
        toilet['divided'] = any([divided, not combined])
    else:
        toilet['divided'] = None
    return toilet


def normalize_balcony(raw_parameters):
    obligatory = len(raw_parameters.get('obligatory', '')) > 0
    preferably = len(raw_parameters.get('preferably', '')) > 0
    balcony = {}
    if obligatory:
        balcony['presence'] = 'obligatory'
    elif preferably:
        balcony['presence'] = 'preferably'
    else:
        balcony['presence'] = None
    return balcony


def normalize_ipoteka(raw_parameters):
    ipoteka = len(raw_parameters.get('needed', '')) > 0
    if ipoteka:
        return True
    return None


def normalize_all_params(raw_parameters):
    facts = {}
    facts['size'] = normalize_size(raw_parameters)
    facts['places'] = normalize_place(raw_parameters)
    facts['price'] = normalize_price(raw_parameters)
    facts['rooms'] = normalize_rooms(raw_parameters)
    facts['undefined'] = get_undefined(raw_parameters)
    facts['undefined_readable'] = normalize_undefined(facts['undefined'])
    facts['possible_places'] = get_possible_places(raw_parameters)
    facts['toilet'] = normalize_toilet(raw_parameters)
    facts['balcony'] = normalize_balcony(raw_parameters)
    facts['ipoteka'] = normalize_ipoteka(raw_parameters)
    return facts
