import json
import sys
from finder import Search

class SearchProducts(Search):

    def load_index(self):
        self.INDEX = {}
        data = open('index/data_product.json')
        for line in data:
            register = json.loads(line)
            self.INDEX.update(register)


import sys

def main():
    if len(sys.argv) == 2 and sys.argv[1] == '-v':
        s = SearchProducts(links=True)
    else:
        s = SearchProducts()
    s.execute()


if __name__ == '__main__':
    main()
