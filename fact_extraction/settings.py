# coding=utf-8
import os

DICTS_DIR = './fact_extraction/tomita_configs/Dicts/'
SUM_ORDER = [
    'thousands',
    'million'
]

# TODO: вытащить квартирность в файлы
GAZETTIER = '''
TAuxDicArticle "Недвижимость"
{{ key = {{ "tomita:{grammars_path}/realty.cxx" type=CUSTOM }} }}

TAuxDicArticle "Цена"
{{ key = {{ "tomita:{grammars_path}/price.cxx" type=CUSTOM }} }}

TAuxDicArticle "Комнатность"
{{ key = {{ "tomita:{grammars_path}/rooms.cxx" type=CUSTOM }} }}

TAuxDicArticle "Место"
{{ key = {{ "tomita:{grammars_path}/place.cxx" type=CUSTOM }} }}

TAuxDicArticle "Площадь"
{{ key = {{ "tomita:{grammars_path}/size.cxx" type=CUSTOM }} }}

TAuxDicArticle "Здравица"
{{ key = {{ "tomita:{grammars_path}/hi.cxx" type=CUSTOM }} }}

TAuxDicArticle "NP"
{{ key = {{ "tomita:{grammars_path}/noun_phrase.cxx" type=CUSTOM }} }}

TAuxDicArticle "Туалет"
{{ key = {{ "tomita:{grammars_path}/toilet.cxx" type=CUSTOM }} }}

TAuxDicArticle "Балкон"
{{ key = {{ "tomita:{grammars_path}/balcony.cxx" type=CUSTOM }} }}

TAuxDicArticle "Ипотека"
{{ key = {{ "tomita:{grammars_path}/ipoteka.cxx" type=CUSTOM }} }}

realty_type "Квартира" {{ key = "квартира" lemma = "квартира" }}
realty_type "Комната" {{ key = "комната" lemma="комната" }}

rooms_w_number "комнат0" {{
    key = 'студия'
    lemma = 'студия'
}}

rooms_w_number "комнат1" {{
    key = 'однушка'
    key = 'однушечка'
    key = 'однуха'
    key = 'однокомнатный'
    key = 'одно-комнатный'
    key = '1-комнатный'
    key = '1-комн'
    key = '1-комнат'
    key = '1-комнатн'
    lemma = '1-комнатная'
}}

rooms_w_number "комнат2" {{
    key = 'двушка'
    key = 'двушечка'
    key = 'двуха'
    key = 'двухкомнатный'
    key = 'двух-комнатный'
    key = '2-комнатный'
    key = '2-комн'
    key = '2-комнат'
    key = '2-комнатн'
    lemma = '2-комнатная'
}}

rooms_w_number "комнат3" {{
    key = 'трешка'
    key = 'трешечка'
    key = 'треха'
    key = 'трехкомнатный'
    key = 'трех-комнатный'
    key = '3-комнатный'
    key = '3-комн'
    key = '3-комнат'
    key = '3-комнатн'
    lemma = '3-комнатная'
}}
rooms_w_number "комнат4" {{
    key = 'четырехкомнатный'
    key = 'четырех-комнатный'
    key = '4-комнатный'
    key = '4-комн'
    key = '4-комнат'
    key = '4-комнатн'
    lemma = '4-комнатная'
}}
rooms_w_number "комнат5" {{
    key = 'пятикомнатный'
    key = 'пяти-комнатный'
    key = '5-комнатный'
    key = '5-комн'
    key = '5-комнат'
    key = '5-комнатн'
    lemma = '5-комнатная'
}}

TAuxDicArticle "отрицание"{{
    key = 'не'
    key = 'кроме'
    lemma = 'не'
}}

TAuxDicArticle "метр" {{
    key = 'м'
    key = 'м2'
    key = 'метр'
    key = 'кв'
    key = 'квадрат'
    lemma = 'метр'
}}
TAuxDicArticle "приветствие" {{
    key = 'hi'
    key = 'Привет'
    key = 'хэй'
    key = 'хай'
    key = 'хэллоу'
    key = 'Здравствуйте'
    key = 'шалом'
    lemma = 'приветствие'
}}
TAuxDicArticle "окончание" {{
    key = 'ух'
    key = 'ех'
    key = 'ти'
    key = 'ку'

    lemma = 'оконч'
}}

number_word 'one' {{
    key = 'один'
    key = 'одно'
    lemma = '1'
}}
number_word 'two' {{
    key = 'два'
    key = 'двух'
    lemma = '2'
}}
number_word 'three' {{
    key = 'три'
    key = 'трех'
    lemma = '3'
}}
number_word 'four' {{
    key = 'четыре'
    key = 'четырех'
    lemma = '4'
}}
number_word 'five' {{
    key = 'пять'
    key = 'пяти'
    lemma = '5'
}}
number_word 'six' {{
    key = 'шесть'
    key = 'шести'
    lemma = '6'
}}
number_word 'seven' {{
    key = 'семь'
    key = 'семи'
    lemma = '7'
}}
number_word 'eight' {{
    key = 'восемь'
    key = 'восьми'
    lemma = '8'
}}
number_word 'nine' {{
    key = 'девять'
    key = 'девяти'
    lemma = '9'
}}
number_word 'ten' {{
    key = 'десять'
    key = 'десяти'
    lemma = '10'
}}
number_word 'eleven' {{
    key = 'одиннадцать'
    key = 'одиннадцати'
    lemma = '11'
}}
number_word 'twelve' {{
    key = 'двендацать'
    key = 'двендацати'
    lemma = '12'
}}
'''
CONFIG = '''
Articles = [ { Name = "Недвижимость" }
             { Name = "Комнатность"}
             { Name = "Цена" }
             { Name = "Место"}
             { Name = "Площадь"}
             { Name = "Здравица"}
             { Name = "NP"}
             { Name = "Туалет"}
             { Name = "Балкон"}
             { Name = "Ипотека" }
             ]
Facts = [
{Name = "RealtyFact"}
{Name = "RoomsFact"}
{Name = "PriceFact"}
{Name = "PlaceFact"}
{Name = "SizeFact"}
{Name = "HelloFact"}
{Name = "NPDebug"}
{Name = "ToiletFact"}
{Name = "BalconyFact"}
{Name = "IpotekaFact"}
]
'''

FACTS = '''
    message RealtyFact: NFactType.TFact { 
        required string type = 1; 
    }
    message RoomsFact: NFactType.TFact {
         required string num_rooms = 1;
    }
    message PlaceFact: NFactType.TFact {
         repeated string place = 1;
         repeated string possible_places = 2;
         optional string total = 3;
    }
    message PriceFact: NFactType.TFact {
         required string price = 1;
         optional string price_min = 2;
         optional string price_max = 3;
         optional string price_about = 4;
    }
    message SizeFact: NFactType.TFact {
         required string total_size = 1;
    }
    message HelloFact: NFactType.TFact {
         required string hi = 1;
    }
    message NPDebug: NFactType.TFact {
         required string debug = 1;
    }
    message ToiletFact: NFactType.TFact {
         optional string divided = 1;
         optional string combined = 2;
         optional string total = 3;
    }
    message BalconyFact: NFactType.TFact {
         optional string obligatory = 1;
         optional string preferably = 2;
         optional string total = 3;
    }
    message IpotekaFact: NFactType.TFact {
         optional string needed = 1;
         optional string total = 3;
    }
'''
KEYWORDS = """
    message realty_type : TAuxDicArticle {};
    message rooms_w_number : TAuxDicArticle {};
    message sum_order : TAuxDicArticle {};
    message geo_1 : TAuxDicArticle {};
    message number_word : TAuxDicArticle {};
    message prefix_words : TAuxDicArticle {};
"""

FACT_DESCRIPTIONS = {
    'RealtyFact': ['type'],
    "RoomsFact": ['num_rooms'],
    "PlaceFact": ['place', "possible_places", "total"],
    "PriceFact": ["price", "price_min", "price_max", "price_about"],
    "SizeFact": ["total_size"],
    "HelloFact": ["hi"],
    "NPDebug": ['debug'],
    "ToiletFact": ['divided', 'combined', 'total'],
    "BalconyFact": ['obligatory', 'preferably', 'total'],
    "IpotekaFact": ['needed', 'total'],
}

PROJECT_PATH = os.environ.get('PROJECT_PATH', '/opt/project/')

SPELLER_DICTS_DIR = PROJECT_PATH + 'speller/data/'
SPELLER_SETTINGS = {
    'counter_filename': SPELLER_DICTS_DIR + 'word_freq_dict.csv.zip',
    'letters_typos_counter_filename': SPELLER_DICTS_DIR + 'letter_typos_matrix.json',
    'typical_typos_filename': SPELLER_DICTS_DIR + 'typical_typos.json',
    'bigrams_filename': SPELLER_DICTS_DIR + 'bigrams.zip',
    'fix_register': False,
    'verbose': False,
    'try_split': True,
    'use_language_model': True,
    'custom_words_file': SPELLER_DICTS_DIR + 'custom_realty_words.csv',
}
