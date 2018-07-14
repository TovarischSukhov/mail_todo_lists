# coding=utf-8
import os

GAZETTIER = '''
TAuxDicArticle "дата"
{
    key = { "tomita:/grammars/date.cxx" type=CUSTOM }
}

TAuxDicArticle "туду"
{
    key = { "tomita:/grammars//todo.cxx" type=CUSTOM }
}

TAuxDicArticle "действие"
{
    key = { "tomita:/grammars/action.cxx" type=CUSTOM }
}

TAuxDicArticle "время"
{
    key = { "tomita:/grammars/time.cxx" type=CUSTOM }
}

month 'jan' {
    key = 'январь'
    key = 'янв'
    key = 'jan'
    lemma = '1'
}
month 'feb' {
    key = 'февраль'
    key = 'фев'
    key = 'feb'
    lemma = '2'
}
month 'march' {
    key = 'март'
    key = 'мар'
    key = 'mar'
    lemma = '3'
}
month 'apr' {
    key = 'апрель'
    key = 'апр'
    key = 'apr'
    lemma = '4'
}
month 'may' {
    key = 'май'
    key = 'may'
    lemma = '5'
}
month 'jun' {
    key = 'июнь'
    key = 'jun'
    lemma = '6'
}
month 'jul' {
    key = 'июль'
    key = 'jul'
    lemma = '7'
}
month 'aug' {
    key = 'август'
    key = 'авг'
    key = 'aug'
    lemma = '8'
}
month 'sent' {
    key = 'сентябрь'
    key = 'сент'
    key = 'sent'
    lemma = '9'
}
month 'okt' {
    key = 'октябрь'
    key = 'окт'
    key = 'okt'
    lemma = '10'
}
month 'nov' {
    key = 'ноябрь'
    key = 'ноя'
    key = 'nov'
    lemma = '11'
}
month 'dec' {
    key = 'декабрь'
    key = 'дек'
    key = 'dec'
    lemma = '12'
}

TAuxDicArticle "месяц"
{
    key = "январь" | "февраль" | "март" | "апрель" | "май" | "июнь" |
          "июль" | "август" |   "сентябрь" | "октябрь" | "ноябрь" | "декабрь"
}

TAuxDicArticle "день_недели"
{
    key = "понедельник" | "вторник" | "среда" | "четверг" | "пятница" | "суббота" | "воскресенье"
}

TAuxDicArticle "время_дня"
{
    key = "утро" | "день" | "вечер" | "ночь" | "обед"
}

number_word 'one' {
    key = 'один'
    key = 'час'
    key = 'первый'
    lemma = '1'
}
number_word 'two' {
    key = 'два'
    key = 'второй'
    lemma = '2'
}
number_word 'three' {
    key = 'три'
    key = 'третий'
    lemma = '3'
}
number_word 'four' {
    key = 'четыре'
    key = 'четвертый'
    lemma = '4'
}
number_word 'five' {
    key = 'пять'
    key = 'пятый'
    lemma = '5'
}
number_word 'six' {
    key = 'шесть'
    key = 'шестой'
    lemma = '6'
}
number_word 'seven' {
    key = 'семь'
    key = 'седьмой'
    lemma = '7'
}
number_word 'eight' {
    key = 'восемь'
    key = 'восьмой'
    lemma = '8'
}
number_word 'nine' {
    key = 'девять'
    key = 'девятый'
    lemma = '9'
}
number_word 'ten' {
    key = 'десять'
    key = 'десятый'
    lemma = '10'
}
number_word 'eleven' {
    key = 'одиннадцать'
    key = 'одиннадцатый'
    lemma = '11'
}
number_word 'twelve' {
    key = 'двендацать'
    key = 'полдень'
    key = 'двенадцатый'
    lemma = '12'
}
number_word 'midnight' {
    key = 'полночь'
    lemma = '00'
}
action 'buy' {
    key = 'купить'
    key = 'закупить'
    key = 'покупать'
    key = 'докупить'
    lemma = 'купить'
}
action 'meeting' {
    key = 'встреча'
    key = 'митинг'
    key = 'разговор'
    key = 'совещание'
    key = 'встретиться'
    lemma = 'встреча'
}
action 'todo' {
    key = 'сделать'
    key = 'дело'
    key = 'делать'
    lemma = 'todo'
}
'''
CONFIG = '''
Articles = [ 
             { Name = "день_недели"}
             { Name = "дата"}
             { Name = "время"}
             { Name = "туду"}
             { Name = "действие"}
             ]
Facts = [
{Name = "DateFact"}
{Name = "TimeFact"}
{Name = "CheckListFact"}
{Name = "ActionFact"}
]
'''

FACTS = '''
    message DateFact: NFactType.TFact { 
        optional string Day = 1; 
        optional string Month = 2;
        optional string Year = 3;
        optional string DayOfWeek = 4;  
    }
    
    message TimeFact: NFactType.TFact { 
        required string type = 1; 
    }
    
    message CheckListFact: NFactType.TFact { 
        required string type = 1; 
    }
    
    message ActionFact: NFactType.TFact { 
        required string type = 1; 
    }
'''
KEYWORDS = """
    message number_word : TAuxDicArticle {};
    message action : TAuxDicArticle {};
    message month : TAuxDicArticle {};
"""

FACT_DESCRIPTIONS = {
    'DateFact': ['type'],
    'TimeFact': ['type'],
    'CheckListFact': ['type'],
    'ActionFact': ['type'],
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
