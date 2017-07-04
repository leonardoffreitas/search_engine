from utils.path_tools import *
from utils.normalizer import Normalizer
from contextlib import contextmanager


def extension_file(file_name=''):
    return splitext(file_name)[1].lower()

ACCEPTABLE_TEXT_FILES = ['.txt', '.html']


class CollectionReader():

    def read_file(self, file_name):
        with open(file_name) as fin:
            for line in fin:
                text = Normalizer().translate_html_entities(line)
                text = Normalizer().normalize_html(text)
                text = Normalizer().normalize_text(text)
                if len(text) > 1: print(text)

    def tracking_documents(self, directories=['docs']):
        for path in directories:
            if is_file(path) and extension_file(path) in ACCEPTABLE_TEXT_FILES:
                self.read_file(path)
            elif is_dir(path):
                path = real_path(path)
                with working_directory(path):
                    self.tracking_documents(list_dir(path))

rf = CollectionReader()
rf.tracking_documents()
