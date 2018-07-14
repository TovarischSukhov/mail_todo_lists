import logging
import os
import os.path as path
import subprocess
import xml.etree.ElementTree
from collections import defaultdict
from io import open

from lxml import html
from string import punctuation

import fact_extraction.tomita_configs.tomita_files_templates as templates


logger = logging.getLogger(__name__)

punctuation += ' '


def write_file(file, content):
    with open(file, 'w', encoding='utf8') as fd:
        fd.write(content)


class TomitaParser(object):

    def __init__(self, directory='/opt/project/fact_extraction/tomita_configs', num_threads=2):
        try:
            self.binary_path = os.environ['TOMITA_PATH']
        except:
            raise KeyError('specify TOMITA_PATH')
        self.grammars_path = os.environ.get('GRAMMARS_PATH', '/grammars/')
        self.project_directory = directory
        
        self.facts_file = path.join(self.project_directory, 'facttypes.proto')
        self.keywords_file = path.join(self.project_directory, 'kwtypes.proto')
        self.gazetteer_file = path.join(self.project_directory, 'dict.gzt')
        self.config_file = path.join(self.project_directory, 'config.proto')
        self.documents_file = path.join(self.project_directory, 'documents_dlp.txt')
        self.output_file = path.join(self.project_directory, 'facts.xml')
        self.num_threads = num_threads

    def write_facts_file(self, facts):
        facts = templates.FACTS.format(facts)
        write_file(self.facts_file, facts)

    def write_keywords_file(self, keywords):
        keywords = templates.KEYWORDS.format(keywords)
        write_file(self.keywords_file, keywords)

    def write_gazetteer_file(self, gazetteer):
        gazetteer = templates.GAZETTEER.format(gazetteer)
        write_file(self.gazetteer_file, gazetteer)

    def write_config_file(self, config):
        config_template = templates.MAIN_CONFIG.format(
            config=config,
            num_threads=self.num_threads
        )
        write_file(self.config_file, config_template)

    def write_message_file(self, message):
        write_file(self.documents_file, message)

    def run(self):
        """
        deletes output file and creates new
        :raises: subprocess.CalledProcessError if tomita parser failed
        :returns: True if run was successful
        """
        if os.path.isfile(self.output_file):
            os.unlink(self.output_file)
        original_dir = os.getcwd()
        try:
            os.chdir(self.project_directory)
            try:
                output = subprocess.check_output(
                    self.binary_path + ' ' + 'config.proto',
                    shell=True,
                    universal_newlines=True,
                    stderr=subprocess.STDOUT,
                )
            except subprocess.CalledProcessError as e:
                logger.debug('Got exception {}'.format(e))
                logger.debug('Tomita output {}'.format(e.output))
                raise e
        finally:
            os.chdir(original_dir)
        success = 'End.  (Processing files.)' in output
        return success

    def get_xml(self):
        """ :return: xml.etree.ElementTree root """
        return xml.etree.ElementTree.parse(self.output_file).getroot()

    def parse(self, fact_descriptions):
        """
        :param fact_descriptions: {'DrivingLicense': ['Category']}
        :return: dict with keys as document id numbers.
        If document doesn't contain facts it just skipped in dictionary

        Example:
        expected_result = {
            1: {'Category': ['C', 'СE']},
            3: {'Category': ['C']}
        }
        """
        root = self.get_xml()
        doc_facts = {}
        for document in root.findall('document'):
            document_id = int(document.attrib['di'])
            doc_facts[document_id] = defaultdict(list)
            facts = document.find('facts')
            for fact_name in fact_descriptions:
                attributes = facts.findall(fact_name)
                for attr in attributes:
                    for attribute_name in fact_descriptions[fact_name]:
                        try:
                            value = attr.find(attribute_name).attrib.get('val')
                            doc_facts[document_id][attribute_name].append(value)
                        except AttributeError:
                            pass
            doc_facts[document_id] = dict(doc_facts[document_id])
            undef_root = html.fromstring(document.find('Leads').find('Lead').attrib['text'])
            undef = []
            for text in undef_root.xpath("//text()"):
                if text.is_tail:
                    undef.append(text.strip())
            doc_facts[document_id]['undefined'] = ' '.join(
                [text for text in undef]
            ).strip()
        return doc_facts
