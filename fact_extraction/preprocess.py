# coding=utf-8
import re

import pymorphy2

MORPH = pymorphy2.MorphAnalyzer()

DIGIT_LETTERS = re.compile('([0-9]+)([А-Яа-яЁё]+)')
PUNCT_LETTERS = re.compile('([А-Яа-яЁё]+[\.|,])([А-Яа-яЁё]+)')
DASH_LETTERS_DIGITS = re.compile('([0-9]+|[А-Яа-яЁё]+)(-)([А-Яа-яЁё]+)')


def get_normal_form(message):
    """
    gets any sequence of words in russian
    :return: specific lemmatized words (gender is saved)
    """
    if isinstance(message, list):
        message = ' '.join(message)
    result = []
    for word in message.split(' '):
        p = MORPH.parse(word)[0]
        gend = p.tag.gender
        if gend:
            result.append(p.inflect({gend, 'sing', 'nomn'}).word)
        else:
            result.append(p.normal_form)
    return ' '.join(result)


def put_needed_spaces(message):
    """
    Put spaces between digit and letters (2ml -> 2 ml)
    Put spaces between punctuation and letters (gg.ml -> gg . ml)
    Put spaces between dashed digits and letters (22-ml -> 22 - ml)
    """
    message = DIGIT_LETTERS.sub(r'\1 \2', message)
    message = PUNCT_LETTERS.sub(r'\1 \2', message)
    message = DASH_LETTERS_DIGITS.sub(r'\1 \2 \3', message)
    return message
