from utils.path_tools import *
from utils.normalizer import Normalizer
from contextlib import contextmanager
from bsddb3 import db
import json
import math

def extension_file(file_name=''):
    return splitext(file_name)[1].lower()

class CollectionReader():

    ACCEPTABLE_TEXT_FILES = ['.txt']

    INDEX = {}  # inverted index
    DOCS_VECTORS = {}  # vectors each doc
    VOCABULARY = {}  # all words exists in collection
    COLLECTION = []

    def _read_file(self, file_name):
        with open(file_name) as fin:
            return fin.read()

    def _add_doc_to_collection(self, doc):
        self.COLLECTION.append(doc)

    def _normalize_text(self, text):
        text = Normalizer().translate_html_entities(text)
        text = Normalizer().normalize_html(text)
        text = Normalizer().normalize_text(text)
        return text

    def _current_tf(self, word, doc):
        if word in self.INDEX and doc in self.INDEX[word]:
            return self.INDEX[word][doc]['tf']
        else:
            return 0

    def _indexer(self, id_doc, text):
        '''Update inverted index'''
        counted = set()
        for word in text.split():
            if word not in counted:
                self.VOCABULARY[word] = self.VOCABULARY.get(word, 0) + 1
                counted.add(word)
            if word not in self.INDEX:
                self.INDEX[word] = {}

            self.INDEX[word][id_doc] = {
                'tf': self._current_tf(word, id_doc) + 1
            }

    def tracking_documents(self, directories=['docs']):

        for possible_doc in directories:

            if (
                is_file(possible_doc) and
                extension_file(possible_doc) in self.ACCEPTABLE_TEXT_FILES
            ):
                doc = real_path(possible_doc)

                self._add_doc_to_collection(doc)

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
        data = db.DB()
        data.open('index/data.db', None, db.DB_HASH, db.DB_CREATE)

        vectors = db.DB()
        vectors.open('index/vectors.db', None, db.DB_HASH, db.DB_CREATE)

        vocabulary = db.DB()
        vocabulary.open('index/vocabulary.db', None, db.DB_HASH, db.DB_CREATE)

        collection_size = len(self.COLLECTION)

        for term in self.INDEX:
            index_key = bytes(term.encode())

            idf = round(math.log(collection_size / self.VOCABULARY[term]), 2)

            for doc in self.INDEX[term]:
                if doc not in self.DOCS_VECTORS:
                    self.DOCS_VECTORS[doc] = {}
                self.DOCS_VECTORS[doc][term] = round(idf * self.INDEX[term][doc]['tf'], 2)

            index_data = json.dumps(self.INDEX[term])
            data.put(
                index_key,
                index_data
            )

            vocabulary.put(
                index_key,
                str(idf)
            )

        data.close()
        vocabulary.close()

        for doc in self.DOCS_VECTORS:
            doc_key = bytes(doc.encode())
            vector = json.dumps(self.DOCS_VECTORS[doc])

            vectors.put(
                doc_key,
                vector
            )
        vectors.close()

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
