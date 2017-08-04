import json
import sys
import math

class Search():

    INDEX = None

    def __init__(self, links=False):
        self.links = links

    def show_results(self, query):
        results = self.find(query)
        docs_per_page = 12
        first_page = 0
        final_page = math.ceil(len(results) / docs_per_page)
        print(final_page, 'resultados encontrados para', query)
        for page_index in range(first_page, final_page):
            print('Página de %d de %d\n' % (page_index+1, final_page))
            page = results[
                (page_index * docs_per_page) : ((page_index+1) * docs_per_page)
            ]

            for doc in page:
                if self.links:
                    print('doc: %s\t\t' % doc.split('/')[-1], '\t\tlink: file://%s' % doc)
                else:
                    print('doc: %s\t' % doc.split('/')[-1])
            print()

            end_pagination = input('Próxima página: enter\nse não: exit\n')
            if end_pagination:
                break

        print('_'*100, '\n')

    def find(self, query_string):
        and_result = None
        words = query_string.split()
        for word in words:
            try:
                results = self.INDEX[word]
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

def main():
    if len(sys.argv) == 2 and sys.argv[1] == '-v':
        s = Search(links=True)
    else:
        s = Search()
    s.execute()

if __name__ == '__main__':
    main()
