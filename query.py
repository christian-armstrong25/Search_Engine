from file_io import read_docs_file, read_title_file, read_words_file
import sys
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))


class Querier():
    """ Takes in user-input searches and outputs the top 10 most relevant pages
    according to the query
    """
    def __init__(self, pagerank : str, titles : str, docs : str, words : str) -> None:
        """ Constructs a Querier that reads in from text files to populate data structures for use
        in providing search results corresponding to user search queries

        Parameters:
        pagerank -- a string designated by "--pagerank" that a user passes in to allow for PageRank influence on search results
        titles -- a text file to read from containing ids to titles
        docs -- a text file to read from containing docs to pageranks
        words -- a text file to read from containing words to docs to relevances
        """
        # initialize and populate corresponding dictionaries from the data read in from the text files
        self.ids_to_titles = {}
        read_title_file(titles, self.ids_to_titles)
        self.ids_to_pageranks = {}
        read_docs_file(docs, self.ids_to_pageranks)
        self.words_to_doc_relevance = {}
        read_words_file(words, self.words_to_doc_relevance)

        print("\n")
        # REPL
        while (True):
            self.ids_to_relevance = {} # initialize here so that search results refresh after every search until quit
            user_input = input("Search: ") # take in user search query

            if user_input == ":quit": # break out of program when quit
                break
            else:
                self.score_docs(user_input.split(), pagerank) # gives docs their score based on user input and optional pagerank
                self.print_top_10() # print top 10 results for user to see

    def score_docs(self, search : list, pagerank : str) -> None:
        """ Gives every page in the corpus a score based on the relevances of each word and their corresponding documents
        while also allowing for pagerank values to influence the scores if requested by the user

        Parameters:
        search -- list of words from the user's search query
        pagerank -- string designated by "--pagerank" that determines whether to influence page scores with pagerank values
        """
        for word in search: # loop through every word given by the user in their search query
            word = PorterStemmer().stem(word) # stem the word
            if word not in STOP_WORDS and word in self.words_to_doc_relevance: # remove stop words and ensure word is in the corpus
                for id in self.words_to_doc_relevance[word]: # loop through every page that the word is found in
                    if id in self.ids_to_relevance: # if the page is already initialized in the dictionary
                        self.ids_to_relevance[id] += self.words_to_doc_relevance[word][id]
                    else:
                        self.ids_to_relevance[id] = 0 # initialize the page's relevance to 0

        if pagerank == "--pagerank": # if "--pagerank" is passed in
            for docs in self.ids_to_relevance: # loop through every document corresponding to the query words
                self.ids_to_relevance[docs] *= self.ids_to_pageranks[docs] # multiply each page's relevance by its pagerank value

    def print_top_10(self):
        """ Prints out the top 10 pages as results for the user's search query
        """
        # sort pages by relevance from highest to lowest
        sorted_list = sorted(self.ids_to_relevance.items(), key= lambda x : x[1], reverse = True)

        # for the top 10 pages, print each one out with its position and title
        for i in range(min(10, len(sorted_list))):
            print(str(i + 1) + ". " + self.ids_to_titles[sorted_list[i][0]])
        print("")

if __name__ == "__main__":
    """ Main method that checks if "--pagerank" is passed in 
    and initializes the Querier with command-line arguments
    """
    command_index = 0
    page_rank = ""
    if sys.argv[1] == "--pagerank":
        command_index = 1
        page_rank = "--pagerank"
    Querier(page_rank, sys.argv[1 + command_index], sys.argv[2 + command_index],sys.argv[3 + command_index])
