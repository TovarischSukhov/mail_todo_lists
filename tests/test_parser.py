# encoding: utf-8

from tests.test_utils import assert_parse_has
from fact_extraction.setup_parser import TomitaRunner


def test_todo_list():
    assert_parse_has("Привет, к завтрашнему дню надо чтобы ты подготовил презентацию и выложил в папку и скинул ссылку в общий чат. После стэндапа сделаем тестовый прогон.", {"facts":[{
        'date': None,
        'time': None,
        'checklist': ["подготовить презентацию", "выложить в дропбокс", "скинуть ссылку в общий чат", "сделать тестовый прогон"],
        'action': 'to-do list'
    }]})


def test_buy_list():
    assert_parse_has("Привет, кончилась еда, нужно купить молоко и сыр, пельмени и сметану", {"facts":[{
        'date': None,
        'time': None,
        'checklist': ["MSI GeForce GTX 1080 Ti GAMING X 11G 8 шт.", "2 AMD Ryzen Threadripper 1950X 8 шт.", "HyperX HX429C17FBK4/64 4 шт."],
        'action': 'купить'
    }]})


def test_meetup():
    assert_parse_has("Привет, назначь встречу с Марком Цукербергом на 20-07-2018 19:00", {"facts":[{
        'date': "20-07-2018",
        'time': "19:00",
        'checklist': [],
        'action': 'встреча'
    }]})

def test_meetup_1():
    assert_parse_has("Привет, назначь встречу с Марком Цукербергом на 2 августа на 10:00", {"facts":[{
        'date': "02-08-2018",
        'time': "10:00",
        'checklist': None,
        'action': 'встреча'
    }]})

if __name__ == "__main__":
    parser = TomitaRunner()
    parser.setup()
    test_meetup_1()
