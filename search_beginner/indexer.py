from utils.path_tools import *
from utils.normalizer import Normalizer
from contextlib import contextmanager
from bsddb3 import db
import json

def extension_file(file_name=''):
    return splitext(file_name)[1].lower()

class CollectionReader():

    ACCEPTABLE_TEXT_FILES = ['.txt', '.html']
    INDEX = {}

    def _read_file(self, file_name):
        with open(file_name) as fin:
            return fin.read()

    def _normalize_text(self, text):
        text = Normalizer().translate_html_entities(text)
        text = Normalizer().normalize_html(text)
        text = Normalizer().normalize_text(text)
        return text

    def tracking_documents(self, directories=['docs']):
        for possible_doc in directories:
            if is_file(possible_doc) and extension_file(possible_doc) in self.ACCEPTABLE_TEXT_FILES:
                doc = real_path(possible_doc)
                self._indexer(
                    doc,
                    self._normalize_text(
                        self._read_file(doc)
                    )
                )
            elif is_dir(possible_doc):
                path = real_path(possible_doc)
                with working_directory(path):
                    self.tracking_documents(list_dir(path))

    def _indexer(self, id_doc, text):
        for word in text.split():
            if word not in self.INDEX:
                self.INDEX[word] = set()
            self.INDEX[word].add(id_doc)

    def save_index(self):
        data = db.DB()
        data.open('index/data.db', None, db.DB_HASH, db.DB_CREATE)
        num_docs = 0
        for term in self.INDEX:
            db_key = bytes(term.encode())
            db_data = json.dumps(list(self.INDEX[term]))
            data.put(
                db_key,
                db_data
            )
            num_docs += 1
            if num_docs % 1000 == 0:
                print(num_docs, 'documentos indexados')
        data.close()
        print(num_docs, 'documentos indexados no total')

    def execute(self):
        self.tracking_documents()
        self.save_index()


cr = CollectionReader()
cr.execute()
