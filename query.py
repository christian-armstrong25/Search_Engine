from file_io import read_docs_file, read_title_file, read_words_file
import sys
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))

class Query:
    def __init__(self) -> None:
        command_index = 0
        if sys.argv[1] == "--pagerank":
            command_index = 1
        self.ids_to_titles = {}
        read_title_file(sys.argv[2 + command_index], self.ids_to_titles)
        self.ids_to_pageranks = {}
        read_docs_file(sys.argv[3 + command_index], self.ids_to_pageranks)
        self.words_to_doc_relevance = {}
        read_words_file(sys.argv[4 + command_index], self.words_to_doc_relevance)
        self.query = []
        self.ids_to_relevance = dict.fromkeys(self.ids_to_titles.keys(), 0)
        
        while (True):
            self.input = input("Search: ")
            if self.input == ":quit":
                break
            else:
                self.score_docs()
                print(self.ids_to_relevance)
    
    def score_docs(self) -> None:
        self.query = self.input.split()
        for word in self.query:
            word = PorterStemmer().stem(word)
            if word not in STOP_WORDS and word in self.words_to_doc_relevance:
                for id in self.words_to_doc_relevance[word]:
                    self.ids_to_relevance[id] += self.words_to_doc_relevance[word][id]
        if sys.argv[1] == "--pagerank":
            for docs in self.ids_to_relevance:
                self.ids_to_relevance[docs] *= self.ids_to_pageranks[docs]

        self.ids_to_relevance = dict(sorted(self.ids_to_relevance.items(), key= lambda x : x[1], reverse = True))

        
        items = self.ids_to_pageranks.items
        for i in items:

            

        

        
    

            
            


