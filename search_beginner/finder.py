from bsddb3 import db

import json
import sys

class Search(object):

    INDEX = None

    def show_results(self, query):
        results = self.find(query)
        first_page = 0
        final_page = len(results)
        docs_per_page = 12

        for page_index in range(first_page, final_page, docs_per_page):
            print('Resultados de %d, à %d\n' % (page_index+1, page_index + docs_per_page))
            page = results[page_index : page_index + docs_per_page]
            for doc in page:
                print(doc)
            print()
            end_pagination = input('Próxima página: enter\nse não: exit\n')
            if end_pagination:
                print('_'*100, '\n')
                break

    def find(self, query_string):
        and_result = None
        terms = query_string.split()
        for term in terms:
            term = bytes(term.encode())
            results = self.INDEX[term].decode('utf-8')
            results = set(json.loads(results))
            if and_result:
                and_result = and_result.intersection(results)
            else:
                and_result = results
        return list(and_result)

    def load_index(self):
        self.INDEX = db.DB()
        self.INDEX.open('index/data.db', None, db.DB_HASH, db.DB_DIRTY_READ)

    def execute(self):

        self.load_index()

        query = input('buscar por: ')
        while query:
            print('Exibindo resultados para: %s' % query)
            self.show_results(query)
            query = input('buscar por: ')

s = Search()
s.execute()
