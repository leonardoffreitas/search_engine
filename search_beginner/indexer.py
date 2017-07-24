from utils.path_tools import *
from utils.normalizer import Normalizer
from contextlib import contextmanager
from bsddb3 import db
import json

def extension_file(file_name=''):
    return splitext(file_name)[1].lower()

ACCEPTABLE_TEXT_FILES = ['.txt', '.html']
INDEX = {}
ID_DOC = 1

class CollectionReader():

    def _read_file(self, file_name):
        with open(file_name) as fin:
            text = Normalizer().translate_html_entities(fin.read())
            text = Normalizer().normalize_html(text)
            text = Normalizer().normalize_text(text)
            if len(text) > 1:
                return (file_name, text)

    def tracking_documents(self, directories=['docs']):
        for path in directories:
            if is_file(path) and extension_file(path) in ACCEPTABLE_TEXT_FILES:
                path = real_path(path)
                self._indexer(*self._read_file(path))
            elif is_dir(path):
                path = real_path(path)
                with working_directory(path):
                    self.tracking_documents(list_dir(path))

    def _indexer(self, file_name, text):
        for term in text.split():
            if term not in INDEX:
                INDEX[term] = set()
            INDEX[term].add(file_name)

    def save_index(self):
        data = db.DB()
        data.open('index/data.db', None, db.DB_HASH, db.DB_CREATE)

        for term in INDEX:
            db_key = bytes(term.encode())
            db_data = json.dumps(list(INDEX[term]))
            data.put(
                db_key,
                db_data
            )
        data.close()

    def execute(self):
        self.tracking_documents()
        self.save_index()


cr = CollectionReader()
cr.execute()
