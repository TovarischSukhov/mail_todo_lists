# coding=utf-8

from fact_extraction.tomita import TomitaParser
from fact_extraction.settings import (
    GAZETTIER, CONFIG, FACTS,
    KEYWORDS
)


class TomitaRunner(TomitaParser):
    def __init__(self, num_threads=2):
        super(TomitaRunner, self).__init__( num_threads=num_threads)
        self.dicts = GAZETTIER#.format(grammars_path=self.grammars_path)

    def generate_dicts(self):
        self.write_gazetteer_file(self.dicts)

    def setup(self):
        self.write_facts_file(FACTS)
        self.write_config_file(CONFIG)
        self.write_keywords_file(KEYWORDS)
        self.generate_dicts()
