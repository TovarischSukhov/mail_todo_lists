# coding=utf-8
import os

DICTS_DIR = './fact_extraction/tomita_configs/Dicts/'

GAZETTIER = '''

TAuxDicArticle "месяц"
{
    key = "январь" | "февраль" | "март" | "апрель" | "май" | "июнь" |
          "июль" | "август" |   "сентябрь" | "октябрь" | "ноябрь" | "декабрь"
}

TAuxDicArticle "день_недели"
{
    key = "понедельник" | "вторник" | "среда" | "четверг" | "пятница" | "суббота" | "воскресенье"
}

TAuxDicArticle "дата"
{
    key = { "tomita::{grammars_path}/date.cxx" type=CUSTOM }
}
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
    message DateFact: NFactType.TFact { 
        required string type = 1; 
    }
    
    message MeetingFact: NFactType.TFact { 
        required string type = 1; 
    }
    
    message TimeFact: NFactType.TFact { 
        required string type = 1; 
    }
    
    message CheckListFact: NFactType.TFact { 
        required string type = 1; 
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
