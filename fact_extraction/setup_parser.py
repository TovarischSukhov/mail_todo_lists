# coding=utf-8
import os

import pandas as pd

from fact_extraction.tomita import TomitaParser
from settings import STOPWORDS
from fact_extraction.settings import (
    DICTS_DIR, SUM_ORDER,
    GAZETTIER, CONFIG, FACTS,
    KEYWORDS
)

os.chdir('/opt/project/')
DATA_DIR = './data/'
STREETS = pd.concat([pd.read_csv(DATA_DIR + f) for f in os.listdir(DATA_DIR)])
STREETS = STREETS.dropna(axis=0, subset=['formalname'])
STREETS = STREETS.drop_duplicates(subset='formalname')

STOPS = []
with open('./fact_extraction/tomita_configs/Dicts/prefixis_words.txt') as f:
    STOPS.extend(f.read().lower().split())
with open('./fact_extraction/tomita_configs/Dicts/stopwords_named.txt') as f:
    STOPS.extend(f.read().lower().split())
STOPS.extend([s.lower() for s in STOPWORDS])


class TomitaRunner(TomitaParser):
    def __init__(self, compile_dk, num_threads=2):
        super(TomitaRunner, self).__init__( num_threads=num_threads)
        self.dicts = GAZETTIER.format(grammars_path=self.grammars_path)
        self.compile_dk = compile_dk

    def generate_dict(self, file_entries, name, lemma, dict_type, possible_invarients):
        grammar_dict = ''
        if lemma:
            grammar_dict = '{} "{}" {{'.format(dict_type, name.split('_')[0])
            for line in file_entries:
                grammar_dict += ' key = "{}"\n'.format(line)
            grammar_dict += ' lemma = "{}"\n'.format(file_entries[0]) + '}\n'
        else:
            for num, line in enumerate(file_entries):
                if possible_invarients and len(line.split(', ')) > 1:
                    invariants = line.split(', ')
                    grammar_dict += '{dict_type} "{name}" {{ lemma = "{f_row}" ' \
                                    'key = "{f_row}" key = "{f_row_lower}" ' \
                                    'key = "{keys}" key = "{keys_lower}" }}\n'.format(
                                        dict_type=dict_type,
                                        name=name.split('_')[0] + str(num),
                                        f_row=invariants[0],
                                        f_row_lower=invariants[0].lower(),
                                        keys='" key="'.join(invariants[1:]),
                                        keys_lower='" key="'.join([inv.lower() for inv in invariants[1:]]),
                                    )
                else:
                    line = line.replace('"', '')
                    line_clean = ' '.join([w for w in line.split(' ') if w.lower() not in STOPS]).strip()
                    long = len(line_clean.split(' ')) > 1
                    w_digit = any(char.isdigit() for char in line_clean)
                    if line_clean and not long and not w_digit:
                        grammar_dict += '{dict_type} "{name}" {{ key = "{key}" ' \
                                        'key = "{key_lower}" lemma = "{lemma}" }}\n '.format(
                                            dict_type=dict_type,
                                            name=name.split('_')[0] + str(num),
                                            key=line_clean,
                                            key_lower=line.lower(),
                                            lemma=line,
                                        )
        return grammar_dict

    def generate_dict_file(self, file_path, name, lemma, dict_type, possible_invarients):
        with open(file_path, encoding='utf-8') as file:
            file_entries = file.read().split('\n')
            grammar_dict = self.generate_dict(file_entries, name, lemma, dict_type, possible_invarients)
        return grammar_dict

    def generate_dicts(self):
        for file in os.listdir(DICTS_DIR):
            named = False
            dict_type = 'TAuxDicArticle'
            postfix = file.split('.')[0].split('_')[-1]
            if postfix == 'named':
                named = True
            if postfix == 'geo':
                dict_type = 'geo_1'
            if postfix == 'words':
                dict_type = 'prefix_words'
            if file.split('_')[0] in SUM_ORDER:
                dict_type = 'sum_order'
            self.dicts += self.generate_dict_file(DICTS_DIR + file, file.split('.')[0],
                                                  named, dict_type, possible_invarients=True)
        if self.compile_dk:
            streets = STREETS.formalname.values.tolist()
            self.dicts += self.generate_dict(streets, name='streets_', lemma=False, dict_type='geo_1',
                                             possible_invarients=False)
        self.write_gazetteer_file(self.dicts)

    def setup(self):
        self.write_facts_file(FACTS)
        self.write_config_file(CONFIG)
        self.write_keywords_file(KEYWORDS)
        self.generate_dicts()
