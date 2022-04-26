from file_io import read_docs_file, read_title_file, read_words_file
import sys
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))

class Query:
    def __init__(self) -> None:
        self.ids_to_titles = {}
        read_title_file(sys.argv[2], self.ids_to_titles)
        self.ids_to_pageranks = {}
        read_docs_file(sys.argv[3], self.ids_to_pageranks)
        self.words_to_doc_relevance = {}
        read_words_file(sys.argv[4], self.words_to_doc_relevance)
        self.query = []
        self.ids_to_relevance = self.ids_to_titles
        while (True):
            self.input = input("Search: ")
            if self.input == ":quit":
                break
            else:
                self.score_docs()
                print(self.ids_to_relevance)
    
    def score_docs(self) -> None:
        stemmer = PorterStemmer()
        self.query = self.input.split()
        for word in self.query:
            if word not in STOP_WORDS:
                word = stemmer.stem(word)
        
        for word in self.words_to_doc_relevance:
            for id in self.words_to_doc_relevance[word]:
                if isinstance(self.ids_to_relevance[id], str):
                    self.ids_to_relevance[id] = self.words_to_doc_relevance[word][id]
                else:
                    self.ids_to_relevance[id] += self.words_to_doc_relevance[word][id]
        self.ids_to_relevance = sorted(self.ids_to_relevance.items(), key= lambda x : x[1], reverse = True)

        # for id in range(0, len(self.ids_to_relevance), 1):
        #     self.ids_to_relevance[id][1] = self.ids_to_titles[id]
        

            
            


