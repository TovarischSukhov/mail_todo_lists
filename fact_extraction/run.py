# coding=utf-8
import logging
import os

from fact_extraction import tomita
from speller.my_speller import Speller
from fact_extraction.preprocess import get_normal_form, put_needed_spaces
from fact_extraction.handle_filters import normalize_all_params
from fact_extraction.settings import FACT_DESCRIPTIONS, SPELLER_SETTINGS

logger = logging.getLogger(__name__)

SPELLER = Speller(**SPELLER_SETTINGS)
# Инициализируем сборку всех файлов спеллера, он собирается при получении первого сообщения
# Первый раз может отвечать вплоть до 20 сек, поэтому запукается заранее
SPELLER('привет')


def preprocess_text(message):
    # TODO: ё на е
    #  Исрпавить опечатки
    message = SPELLER(message)
    # поставить пробелы
    message = put_needed_spaces(message)
    return message


def tomita_parse_message(message):
    logger.debug('Parsing message {}'.format(message))
    parser = tomita.TomitaParser()
    parser.write_message_file(message)
    parser.run()
    result = parser.parse(FACT_DESCRIPTIONS).get(1, {})
    return result


def custom_extend_dict(dict1, dict2):
    """
    Gets 2 dicts, where values are lists
    Extending first with second.
    If there are common keys, the values of this keys in resulting dict
    will be extended list of values from both dicts
    :param dict1: base dict
    :param dict2: dict with additional values
    :return: updated dict
    """
    common_keys = set([*dict1]).intersection([*dict2])
    for key in common_keys:
        if dict1[key] == dict2[key]:
            continue
        if not dict1[key]:
            dict1[key] = dict2[key]
        else:
            if isinstance(dict2[key], dict) and isinstance(dict1[key], dict):
                dict2[key] = custom_extend_dict(dict1[key], dict2[key])
            elif isinstance(dict1[key], dict):
                dict2[key] = dict1[key]
            elif not isinstance(dict1[key], list):
                if dict1[key]:
                    dict2[key] = dict1[key]
            else:
                dict1[key].extend(dict2[key])
        dict2.pop(key)

    dict1.update(dict2)
    return dict1


def extract_facts(message):
    # предобработка
    logger.debug('Start preprocess')
    message = preprocess_text(message)

    # запуск томиты
    logger.debug('Start tomita')
    result = tomita_parse_message(message)

    # постобработка фильтров, приведение в стандартный вид
    raw_parameters = result
    logger.debug('Start postprocess')
    facts = normalize_all_params(raw_parameters)
    if facts['undefined']:
        logger.debug('Start tomita second loop')
        try_normal_form = tomita_parse_message(get_normal_form(facts['undefined']))
        if try_normal_form != {}:
            logger.debug('Start postprocess second loop')
            facts.pop('undefined_readable')
            facts = custom_extend_dict(facts, normalize_all_params(try_normal_form))
    logger.debug('finish')
    return facts
