from utils.path_tools import *
from utils.normalizer import Normalizer
import json

def extension_file(file_name=''):
    return splitext(file_name)[1].lower()

class CollectionReader():

    ACCEPTABLE_TEXT_FILES = ['.html']

    INDEX = {}  # inverted index

    def _read_file(self, file_name):
        with open(file_name) as fin:
            return fin.read()

    def _normalize_text(self, text):
        text = Normalizer().translate_html_entities(text)
        text = Normalizer().normalize_html(text)
        text = Normalizer().normalize_text(text)
        return text


    def _indexer(self, id_doc, text):
        '''Update inverted index'''
        for word in text.split():
            if word not in self.INDEX:
                self.INDEX[word] = set()

            self.INDEX[word].add(id_doc)

    def tracking_documents(self, directories=['docs']):

        for possible_doc in directories:

            if (
                is_file(possible_doc) and
                extension_file(possible_doc) in self.ACCEPTABLE_TEXT_FILES
            ):
                doc = real_path(possible_doc)
                self._indexer(
                    doc,
                    self._normalize_text(
                        self._read_file(doc)
                    )
                )
                self.num_docs += 1
                if self.num_docs % 1000 == 0:
                    print(self.num_docs, 'documentos indexados')
            elif is_dir(possible_doc):
                path = real_path(possible_doc)
                with working_directory(path):
                    self.tracking_documents(list_dir(path))

    def save_index(self):
        data = open('index/data.json', 'w')

        for word in self.INDEX:
            index_key = word

            index_data = list(self.INDEX[word])
            payload = json.dumps({index_key: index_data})
            print (payload, file=data)

        data.close()

    def execute(self):
        print('Starting indexing')
        self.num_docs = 0
        self.tracking_documents()
        self.save_index()
        print(self.num_docs, 'documentos indexados no total')

def main():
    cr = CollectionReader()
    cr.execute()

if __name__ == '__main__':
    main()
