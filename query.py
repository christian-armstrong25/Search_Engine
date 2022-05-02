from file_io import read_docs_file, read_title_file, read_words_file
import sys
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))


class Querier():
    def __init__(self, pagerank, titles, docs, words) -> None:
        self.ids_to_titles = {}
        read_title_file(titles, self.ids_to_titles)
        self.ids_to_pageranks = {}
        read_docs_file(docs, self.ids_to_pageranks)
        self.words_to_doc_relevance = {}
        read_words_file(words, self.words_to_doc_relevance)
        print("\n")
        while (True):
            self.ids_to_relevance = {}
            user_input = input("Search: ")
            if user_input == ":quit":
                break
            else:
                self.score_docs(user_input.split(), pagerank)
                self.print_top_10()

    def score_docs(self, search, pagerank) -> None:
        for word in search:
            word = PorterStemmer().stem(word)
            if word not in STOP_WORDS and word in self.words_to_doc_relevance:
                for id in self.words_to_doc_relevance[word]:
                    if id in self.ids_to_relevance:
                        self.ids_to_relevance[id] += self.words_to_doc_relevance[word][id]
                    else:
                        self.ids_to_relevance[id] = 0
        if pagerank == "--pagerank":
            for docs in self.ids_to_relevance:
                self.ids_to_relevance[docs] *= self.ids_to_pageranks[docs]

    def print_top_10(self):
        sorted_list = sorted(self.ids_to_relevance.items(), key= lambda x : x[1], reverse = True)
        for i in range(min(10, len(sorted_list))):
            print(str(i + 1) + ". " + self.ids_to_titles[sorted_list[i][0]])
        print("")

if __name__ == "__main__":
    command_index = 0
    page_rank = ""
    if sys.argv[1] == "--pagerank":
        command_index = 1
        page_rank = "--pagerank"
    Querier(page_rank, sys.argv[1 + command_index], sys.argv[2 + command_index],sys.argv[3 + command_index])
