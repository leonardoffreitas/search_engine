from indexer import CollectionReader
from utils.path_tools import *
import json
import math

def extension_file(file_name=''):
    return splitext(file_name)[1].lower()

class ProductsIndexer(CollectionReader):

    ACCEPTABLE_TEXT_FILES = ['.json']
    def tracking_documents(self, directories=['docs']):
        for possible_file in directories:
            if is_file(possible_file) and extension_file(possible_file) in self.ACCEPTABLE_TEXT_FILES:
                file_name = real_path(possible_file)
                file_to_index = open(file_name)
                for doc in file_to_index:
                    try:
                        doc_id = json.loads(doc)['title']
                    except:
                        continue
                    self.COLLECTION.append(doc)
                    self._indexer(
                        doc_id,
                        self._normalize_text(
                            doc
                        )
                    )
                    self.num_docs += 1
                    if self.num_docs % 1000 == 0:
                        print(self.num_docs, 'documentos indexados')
                file_to_index.close()
            elif is_dir(possible_file):
                path = real_path(possible_file)
                with working_directory(path):
                    self.tracking_documents(list_dir(path))


def main():
    pi = ProductsIndexer()
    pi.execute()

if __name__ == '__main__':
    main()


