import json
import sys

class Search():

    INDEX = None

    def __init__(self, links=False):
        self.links = links

    def show_results(self, query):
        results = self.find(query)
        first_page = 0
        final_page = len(results)
        docs_per_page = 12
        print(final_page, 'resultados encontrados para', query)
        for page_index in range(first_page, final_page, docs_per_page):
            print('Resultados de %d à %d\n' % (page_index+1, page_index + docs_per_page))
            page = results[page_index : page_index + docs_per_page]
            for doc in page:
                if self.links:
                    print('file: %s\t\t' % doc.split('/')[-1], '\t\tlink: file://%s' % doc)
                else:
                    print('file: %s\t' % doc.split('/')[-1])
            print()
            end_pagination = input('Próxima página: enter\nse não: exit\n')
            if end_pagination:
                break
        print('_'*100, '\n')

    def find(self, query_string):
        and_result = None
        terms = query_string.split()
        for term in terms:
            try:
                results = self.INDEX[term]
                results = set(results)
            except:
                results = set()
            if and_result:
                and_result = and_result.intersection(results)
            else:
                and_result = results
        return list(and_result)

    def load_index(self):
        self.INDEX = {}
        data = open('index/data.json')
        for line in data:
            register = json.loads(line)
            self.INDEX.update(register)

    def execute(self):

        self.load_index()

        query = input('buscar por: ')
        while query:
            self.show_results(query)
            query = input('buscar por: ')

import sys

if len(sys.argv) == 2 and sys.argv[1] == '-v':
    s = Search(links=True)
else:
    s = Search()
s.execute()
