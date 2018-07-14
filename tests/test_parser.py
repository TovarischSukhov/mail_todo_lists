# encoding: utf-8

import pytest

from fact_extraction.setup_parser import TomitaRunner
from tests.test_utils import assert_parse_has

parser = TomitaRunner(True)
parser.setup()  # rebuild dicts


def test_rooms_single_letters_alias():
    assert_parse_has('Хочу трешку', {'rooms': ['3']})
    assert_parse_has('Хочу студию', {'rooms': ['st']})
    assert_parse_has('Хочу двушку', {'rooms': ['2']})
    assert_parse_has('Хочу однушку', {'rooms': ['1']})
    assert_parse_has('Хочу двуху', {'rooms': ['2']})


def test_rooms_single_letters_word_spaced():
    assert_parse_has('Хочу трех комнатную квартиру', {'rooms': ['3']})


def test_rooms_single_letters_word():
    assert_parse_has('Хочу трехкомнатную квартиру', {'rooms': ['3']})


def test_rooms_single_letters_n_rooms():
    assert_parse_has('Хочу квартиру четыре комнаты', {'rooms': ['4']})


def test_rooms_multiple_letters_alias():
    assert_parse_has('Хочу студию и однушку', {'rooms': ['1', 'st']})


def test_rooms_single_digits_dashed():
    assert_parse_has('Хочу 2-комнатную', {'rooms': ['2']})
    assert_parse_has('Хочу 2-комн', {'rooms': ['2']})
    assert_parse_has('Хочу 2ух-комнатную', {'rooms': ['2']})
    assert_parse_has('Хочу 2-ку', {'rooms': ['2']})


def test_rooms_single_digits_spaced():
    assert_parse_has('Хочу 2комнатную', {'rooms': ['2']})
    assert_parse_has('Хочу 2ухкомнатную', {'rooms': ['2']})


def test_rooms_single_digits_n_rooms():
    assert_parse_has('Хочу квартиру 5 комнат', {'rooms': ['5']})


def test_rooms_multiple_letters_dash_space_combined():
    assert_parse_has('Хочу двух-трехкомнатную квартиру', {'rooms': ['2', '3']})
    assert_parse_has('Хочу двух-трех комнатную квартиру', {'rooms': ['2', '3']})


def test_rooms_multiple_digits_dashed():
    assert_parse_has('Хочу 1-2-3комн', {'rooms': ['1', '2', '3']})


def test_rooms_multiple_digits_dash_space_combined():
    assert_parse_has('Хочу 2 ух или 3ех комнатную квартиру', {'rooms': ['2', '3']})
    assert_parse_has('Хочу 2 ух или 3ех или 5ти комнатную квартиру', {'rooms': ['2', '3', '5']})
    assert_parse_has('Хочу 2 ух или 3ех-комнатную квартиру', {'rooms': ['2', '3']})


def test_price_one_letters():
    assert_parse_has('Хочу 1комнатный за два млн',
                     {"price": {'price_about': 2000000}, "rooms": ["1"]})


def test_price_one_letters_multiplier():
    assert_parse_has('Хочу 5комнатный за пять кк',
                     {"price": {'price_about': 5000000}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный за три лимона',
                     {"price": {'price_about': 3000000}, 'rooms': ['5']})


def test_price_several_letters():
    assert_parse_has('Хочу 1комнатный за два-три млн',
                     {"price": {'price_about': [2000000, 3000000]}, 'rooms': ['1']})


@pytest.mark.skip(reason="пока не поддерживается")
def test_price_no_number():
    assert_parse_has('Хочу 1комнатный за миллион',
                     {'price_min': 900000, 'price_max': 1100000, 'rooms': ['1']})
    assert_parse_has('Хочу 1комнатный за млн',
                     {'price_min': 900000, 'price_max': 1100000, 'rooms': ['1']})


def test_price_about():
    assert_parse_has('Хочу 1комнатный около 2 млн',
                     {"price": {'price_about': 2000000}, 'rooms': ['1']})
    assert_parse_has('Хочу 1комнатный, 3000000',
                     {"price": {'price_about': 3000000}, 'rooms': ['1']})


def test_price_int_multiplier():
    assert_parse_has('Хочу 1комнатный до 5 млн',
                     {"price": {'price_max': 5000000}, 'rooms': ['1']})
    assert_parse_has('Хочу 5комнатный за 3800 к',
                     {"price": {'price_about': 3800000}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный за 1 лимон',
                     {"price": {'price_about': 1000000}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный за 5 кк',
                     {"price": {'price_about': 5000000}, 'rooms': ['5']})


def test_price_int_multiplier_custom():
    assert_parse_has('Хочу 5комнатный за 3 ляма',
                     {"price": {'price_about': 3000000}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный за 3 лимона',
                     {"price": {'price_about': 3000000}, 'rooms': ['5']})  # TODO: fix test
    assert_parse_has('Хочу 5комнатный за три лимона',
                     {"price": {'price_about': 3000000}, 'rooms': ['5']})  # TODO: fix test
    assert_parse_has('Хочу 5комнатный за 5 лямов',
                     {"price": {'price_about': 5000000}, 'rooms': ['5']})  # TODO: fix test
    assert_parse_has('Хочу 5комнатный за 3800 тонн',
                     {"price": {'price_about': 3800000}, 'rooms': ['5']})  # TODO: fix test
    assert_parse_has('Хочу 5комнатный за 3800 кусков',
                     {"price": {'price_about': 3800000}, 'rooms': ['5']})  # TODO: fix test


def test_price_several_int_one_multiplier():
    assert_parse_has('Хочу 5комнатный от 3 до 5 млн',
                     {"price": {'price_min': 3000000, 'price_max': 5000000}, 'rooms': ['5']})


def test_price_several_int_several_multiplier():
    assert_parse_has('Хочу 5комнатный от 900 тыс до 5 млн',
                     {"price": {'price_min': 900000, 'price_max': 5000000}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный от 900тыс до 5млн',
                     {"price": {'price_min': 900000, 'price_max': 5000000}, 'rooms': ['5']})


def test_price_float_multiplier():
    assert_parse_has('Хочу 5комнатный в районе 5,6 млн',
                     {"price": {'price_about': 5600000}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный около 5,03 млн',
                     {"price": {'price_about': 5030000}, 'rooms': ['5']})


def test_price_several_int():
    assert_parse_has('Хочу 5комнатный за 5 000 000',
                     {"price": {'price_about': 5000000}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный за 5000000',
                     {"price": {'price_about': 5000000}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный, 5000000',
                     {"price": {'price_about': 5000000}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный, 5 000000',
                     {"price": {'price_about': 5000000}, 'rooms': ['5']})


def test_place_solo_one_word_area_noun():
    assert_parse_has('Хочу 5комнатный от 50 квадратов за 5 кк в бирюлево',
                     {'size': {'total': 50}, 'rooms': ['5'], 'price': {'price_about': 5000000},
                      'places': [{'location': 'БИРЮЛЁВО'}]})
    assert_parse_has('Хочу 1комнатный в строгино',
                     {'places': [{'location': 'СТРОГИНО'}], 'rooms': ['1']})
    assert_parse_has('Хочу 1комнатный в измайлово',
                     {'places': [{'location': 'ИЗМАЙЛОВО'}], 'rooms': ['1']})


def test_place_solo_one_word_named_area_noun():
    assert_parse_has('Хочу 1комнатный район измайлово',
                     {'places': [{'location': 'ИЗМАЙЛОВО'}], 'rooms': ['1']})
    # assert_parse_has('Хочу 1комнатный недалеко от метро перово',
    #                  {'places': [{'location': 'ПЕРОВО'}], 'rooms': ['1']})
    assert_parse_has('Хочу 1комнатный м перово',
                     {'places': [{'location': 'ПЕРОВО'}], 'rooms': ['1']})
    assert_parse_has('Хочу 1комнатный в районе метро Кутузовская',
                     {'places': [{'location': 'КУТУЗОВСКАЯ'}], 'rooms': ['1']})


@pytest.mark.skip(reason="wtf")
def test_place_solo_one_word_named_area_prefix():
    assert_parse_has('Хочу 1комнатный в районе китай-города',
                     {'place': ['В РАЙОНЕ ЮЖНОГО ИЗМАЙЛОВО'], 'rooms': ['1']})
    assert_parse_has('Хочу 1комнатный в районе южного измайлово',
                     {'place': ['В РАЙОНЕ ЮЖНОГО ИЗМАЙЛОВО'], 'rooms': ['1']})  # TODO FIX


def test_place_solo_one_word_area_adj():
    assert_parse_has('Хочу 5комнатный от 50 квадратов за 5 кк на Петроградской',
                     {'size': {'total': 50}, 'rooms': ['5'], 'price': {'price_about': 5000000},
                      'places': [{'location': 'ПЕТРОГРАДСКАЯ'}]})
    assert_parse_has('Хочу двушку на пушкинской',
                     {'places': [{'location': 'ПУШКИНСКАЯ'}], 'rooms': ['2']})


def test_place_solo_one_word_street():
    assert_parse_has('Хочу двушку на Ильинке',
                     {'places': [{'location': 'ИЛЬИНКА'}], 'rooms': ['2']})
    assert_parse_has('Хочу двушку на ильинке',
                     {'places': [{'location': 'ИЛЬИНКА'}], 'rooms': ['2']})
    assert_parse_has('Хочу 1комнатный ул Первомайская',
                     {'places': [{'location': 'ПЕРВОМАЙСКАЯ'}], 'rooms': ['1']})


@pytest.mark.skip(reason="wtf")
def test_wtf_place_solo_one_word_street():
    assert_parse_has('Хочу двушку на кутузовском проспекте',
                     {'places': [{'location': 'КУТУЗОВСКИЙ'}], 'rooms': ['2']})  # TODO: разобраться с проспектом


def test_place_solo_several_words_area():
    assert_parse_has('Хочу двушку на марьиной роще',
                     {'places': [{'location': 'МАРЬИНА РОЩА'}], 'rooms': ['2']})


def test_place_several_combined():
    assert_parse_has('ищу однушку около метро кутузовская, хамовники, перово',
                     {'places': [{'location': 'КУТУЗОВСКАЯ'},
                                 {'location': 'ХАМОВНИКИ'},
                                 {'location': 'ПЕРОВО'}],
                      'rooms': ['1']})


def test_place_city():
    assert_parse_has('Хочу студию в Москве',
                     {'places': [{'location': 'МОСКВА'}], 'rooms': ['st']})


def test_size():
    assert_parse_has('Хочу 5комнатный от 50 квадратов за 5 кк',
                     {'size': {'total': 50}, 'rooms': ['5'], 'price': {'price_about': 5000000}})
    assert_parse_has('Хочу 5комнатный от 50 квадратов',
                     {'size': {'total': 50}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный от 55 кв.м',
                     {'size': {'total': 55}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный от 60 метров',
                     {'size': {'total': 60}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный от 65 м.кв',
                     {'size': {'total': 65}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный от 70м',
                     {'size': {'total': 70}, 'rooms': ['5']})
    assert_parse_has('Хочу 5комнатный от 80 м',
                     {'size': {'total': 80}, 'rooms': ['5']})


def test_undefined():
    assert_parse_has('Хочу 5комнатный от 50 квадратов за 5 кк не бабушкин вариант',
                     {'size': {'total': 50}, 'rooms': ['5'], 'price': {'price_about': 5000000},
                      'undefined_readable': 'не бабушкин вариант'})
    assert_parse_has('Хочу квартиру где-нибудь',
                     {'undefined_readable': 'где  нибудь'})


# Тест не актаулен, так как мусор убирается теперь только при выводе пользвателю
# def test_undefined_no_trash():
#     assert_parse_has('Хочу двушечку, от 10 милионов, в биберево!',
#                      {'price_min': 10 ** 7, 'price_max': 0, 'rooms': ['2'], 'undefined': ''})
#     assert_parse_has('Хочу двушечку, от 10 милионов, в биберево! за от к',
#                      {'price_min': 10 ** 7, 'price_max': 0, 'rooms': ['2'], 'undefined': ''})


def test_from_price():
    assert_parse_has('Хочу двушечку от 10 млн в марьиной роще',
                     {'price': {'price_min': 10000000, 'price_max': 0}, 'rooms': ['2'],
                      'places': [{'location': 'МАРЬИНА РОЩА'}]})


def test_mistypes():
    assert_parse_has('Хочу двушечку от 10 милионов в биберево',
                     {'price': {'price_max': 0, 'price_min': 10000000}, 'rooms': ['2'],
                      'places': [{'location': 'БИБИРЕВО'}]})
    assert_parse_has('Хочу петикомнатную от 10 милионов в хмиках',
                     {'price': {'price_max': 0, 'price_min': 10000000}, 'rooms': ['5'],
                      'places': [{'location': 'ХИМКИ'}]})


def test_possible_places():
    assert_parse_has('Хочу двушечку около МГУ',
                     {'possible_places': [{'location': 'МГУ'}], 'places': [], 'rooms': ['2']})
    assert_parse_has('Хочу двушечку около школы 1283',
                     {'possible_places': [{'location': 'ШКОЛА 1283'}], 'rooms': ['2']})
    assert_parse_has('Хочу двушечку около бородинской панорамы',
                     {'possible_places': [{'location': 'БОРОДИНСКАЯ ПАНОРАМА'}], 'rooms': ['2']})
    assert_parse_has('Хочу двушечку рядом с Красной Площадью',
                     {'possible_places': [{'location': 'КРАСНАЯ ПЛОЩАДЬ'}], 'rooms': ['2']})
    assert_parse_has('хочу квартиру рядом со второй школой',
                     {'possible_places': [{'location': 'ВТОРАЯ ШКОЛА'}]})
    assert_parse_has('Хочу двушечку рядом с первым лицеем',
                     {'possible_places': [{'location': 'ПЕРВЫЙ ЛИЦЕЙ'}], 'rooms': ['2']})
    assert_parse_has('Хочу двушечку около Лефортовского сквера',
                     {'possible_places': [{'location': 'ЛЕФОРТОВСКИЙ СКВЕР'}], 'rooms': ['2']})
    assert_parse_has('Хочу двушечку около Метрополиса',
                     {'possible_places': [{'location': 'МЕТРОПОЛИС'}], 'rooms': ['2']})
    assert_parse_has('Хочу двушечку около памятника Пушкина',
                     {'possible_places': [{'location': 'ПАМЯТНИК ПУШКИНА'}], 'rooms': ['2']})
    # assert_parse_has('Хочу двушечку около памятника Пушкину',
    #                  {'possible_places': [{'location': 'ПАМЯТНИК ПУШКИНА'}], 'rooms': ['2']})


def test_toilet_combined():
    assert_parse_has('Хочу двушечку со слитным санузлом',
                     {'toilet': {'divided': False}, 'rooms': ['2']})
    # assert_parse_has('Хочу двушечку с объединенный санузел',
    #                  {'toilet': {'divided': False}, 'rooms': ['2']})
    assert_parse_has('Хочу двушечку. туалет должен быть слитным',
                     {'toilet': {'divided': False}, 'rooms': ['2']})


def test_toilet_divided():
    assert_parse_has('Хочу двушечку с раздельным санузлом',
                     {'toilet': {'divided': True}, 'rooms': ['2']})
    assert_parse_has('Хочу двушечку. туалет должен быть раздельным',
                     {'toilet': {'divided': True}, 'rooms': ['2']})
    assert_parse_has('Хочу двушечку. санузел должен быть раздельным',
                     {'toilet': {'divided': True}, 'rooms': ['2']})


def test_obligatory_balcony():
    assert_parse_has('Хочу двушечку с балконом',
                     {'balcony': {'presence': 'obligatory'}, 'rooms': ['2']})
    assert_parse_has('Хочу двушечку, обязательно с балконом',
                     {'balcony': {'presence': 'obligatory'}, 'rooms': ['2']})
    assert_parse_has('Хочу двушечку, наличие балкона важно',
                     {'balcony': {'presence': 'obligatory'}, 'rooms': ['2']})
    assert_parse_has('Хочу двушечку, важно наличие балкона',
                     {'balcony': {'presence': 'obligatory'}, 'rooms': ['2']})


def test_preferably_balcony():
    assert_parse_has('Хочу двушечку желательно с балконом',
                     {'balcony': {'presence': 'preferably'}, 'rooms': ['2']})
    assert_parse_has('Хочу двушечку, желательно наличие балкона',
                     {'balcony': {'presence': 'preferably'}, 'rooms': ['2']})
    assert_parse_has('Хочу двушечку, желательно с лоджией или балконом',
                     {'balcony': {'presence': 'preferably'}, 'rooms': ['2']})
    assert_parse_has('Хочу двушечку, наличие лоджии или балкона желательно',
                     {'balcony': {'presence': 'preferably'}, 'rooms': ['2']})


def test_ipoteka():
    assert_parse_has('Хочу двушечку, в кредит',
                     {'ipoteka': True, 'rooms': ['2']})
    assert_parse_has('Хочу двушечку доступную в ипотеку',
                     {'ipoteka': True, 'rooms': ['2']})
