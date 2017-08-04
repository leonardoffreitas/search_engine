from bsddb3 import db

import operator
import json
import sys
import math

class Search():

    INDEX = None
    VOCABULARY = None
    VECORS = None

    def __init__(self, links=False):
        self.links = links

    def _ranking_function(self, query_vector, result):
        distance_docs = {}
        for doc in result:
            doc_key = bytes(doc.encode())
            print(doc)
            print(query_vector)
            print(self.VECTORS.keys())
            print( self.VECTORS[doc_key])
            print ()
            distance = self.similarity(query_vector, json.loads(self.VECTORS[doc_key].decode('utf-8')))
            distance_docs[doc + ' - distance: ' + str(distance)] = distance
        sorted_ranking = sorted(distance_docs.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_ranking


    def show_results(self, query):
        results = self.find(query)
        docs_per_page = 12
        first_page = 0
        final_page = math.ceil(len(results) / docs_per_page)
        print(final_page, 'resultados encontrados para', query)
        for page_index in range(first_page, final_page):
            print('Página de %d de %d\n' % (page_index+1, final_page))
            page = results[
                page_index * docs_per_page :
                (page_index+1) * docs_per_page]
            for doc in page:
                if self.links:
                    print('doc: %s\t\t' % doc[0].split('/')[-1], '\t\tlink: file://%s' % doc[0])
                else:
                    print('doc: %s\t' % doc[0].split('/')[-1])
            print()
            end_pagination = input('Próxima página: enter\nse não: exit\n')
            if end_pagination:
                break
        print('_'*100, '\n')

    def similarity(self, vec1, vec2):
        def pitagoras(vec):
            total = 0
            print(vec.values())
            for d in vec:
                total = total + math.pow(vec[d], 2)
            return math.sqrt(total)
        print(vec1)
        print(vec2)
        intersection = set.intersection(
            set(vec1.keys()),
            set(vec2.keys())
        )

#        if len(vec2) == 1:
#        vec1[b'0'] = 0
#        vec2[b'0'] = 0
#            return math.sqrt(math.pow(vec1[b'brazil'], 2) + math.pow(vec2[b'brazil'], 2))
        vector_norm = 0
        for term in intersection:
            vector_norm = vector_norm + (vec1[term]*vec2[term])
            print(vector_norm)
        vector_prod = pitagoras(vec1) * pitagoras(vec2)
        print(vector_norm)
        print('--------')
        print(vector_prod)
        return vector_norm / vector_prod

    def find(self, query_string):
        and_result = None
        terms = query_string.split()

        vectors_docs = {}
        vector_query = {}

        for term in terms:
            term_key = bytes(term.encode())

            if term_key in self.VOCABULARY:
                vector_query[term] = float(self.VOCABULARY[term_key])
            else:
                vector_query[term] = 1.0

            try:
                # find all docs that content current term
                results = self.INDEX[term_key].decode('utf-8')
                results = json.loads(results)
                # docs with current term
                results = set(results)
            except Exception as e:
                results = set()
            # only 'AND result'
            if and_result:
                and_result = and_result.intersection(results)
            else:
                and_result = results
        # removing vectors out of 'AND result'
        return self._ranking_function(vector_query, and_result)

    def load_index(self):
        self.INDEX = db.DB()
        self.INDEX.open(
            'index/data.db',
            None,
            db.DB_HASH,
            db.DB_DIRTY_READ
        )

        self.VOCABULARY = db.DB()
        self.VOCABULARY.open(
            'index/vocabulary.db',
            None,
            db.DB_HASH,
            db.DB_DIRTY_READ
        )

        self.VECTORS = db.DB()
        self.VECTORS.open(
            'index/vectors.db',
            None,
            db.DB_HASH,
            db.DB_DIRTY_READ
        )

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
