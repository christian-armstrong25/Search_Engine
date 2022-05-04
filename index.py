from ipaddress import summarize_address_range
import sys
import xml.etree.ElementTree as et
import re
from file_io import write_docs_file, write_title_file, write_words_file
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import math
STOP_WORDS = set(stopwords.words('english'))


class Indexer:
    """ Parses an xml and calculates relevance and pagerank values 
    to use for the querier in the search engine
    """
    def __init__(self, xml : str, titles : str, docs : str, words : str) -> None:
        """ Constructs an Indexer that initializes important data structures and writes to three text files
        with parsed and calculated data

        Parameters:
        xml -- xml file to parse for data
        titles -- the text file to write to with ids to titles
        docs -- the text file to write to with ids to pageranks
        words -- the text file to write to with words to docs to relevances
        """
        self.ids_to_titles = {}  # maps page ids to page titles
        self.ids_links_titles = {}  # maps an id to all the titles it links to
        self.ids_to_pageranks = {}  # maps ids to pageranks
        self.words_to_doc_relevance = {} # double dictionary from words to docs to correponding relevance
        self.EPSILON = 0.15
        self.DELTA = 0.001

        self.parse(xml)
        self.TOTAL_DOCS = len(self.ids_to_titles) 
        self.calc_relevance()
       
        self.weight_dictionary = {} # double dictionary of ids to ids to the weights of the ids' links
        self.calc_weight()
        self.page_rank()
        self.sum = sum(self.ids_to_pageranks.values()) # store the sum of pageranks to ensure they add up to 1
        
        write_title_file(titles, self.ids_to_titles)
        write_docs_file(docs, self.ids_to_pageranks)
        write_words_file(words, self.words_to_doc_relevance)

    def parse(self, input_file : str) -> None:
        """ Parses, stems, tokenizes, removes stop words, maps ids to titles, stores linking relationships,
        and calculates relevance through term frequency and inverse-document frequency

        Parameters:
        input_file -- the xml file to parse
        """
        # two separate regexs, one for links and one for text
        link_regex = '''\[\[[^\[]+?\]\]'''
        text_regex = '''[a-zA-Z]+'[a-zA-Z]+|[a-zA-Z]+'''

        wiki_tree = et.parse(input_file)
        wiki_xml_root = wiki_tree.getroot()

        for wiki_page in wiki_xml_root:

            page_id = int(wiki_page.find('id').text.strip()) # id of current page

            words = [] # list of all the words in the current page
            self.word_count_in_page = {} # dictionary from word to count on current page

            # adds the current page's id and title to the ids_to_titles dictionary
            self.ids_to_titles[page_id] = wiki_page.find(
                'title').text.strip()

            # tokenize words
            words.extend(re.findall(text_regex, wiki_page.find(
                'text').text.strip().lower()))  # adds words from texts
            words.extend(re.findall(text_regex, wiki_page.find(
                'title').text.strip().lower()))  # adds words from titles

            self.ids_links_titles[page_id] = [] # fill up linking dictionary with empty lists
            self.remove_link_words = [] # list of words to remove from corpus

            # removes brackets from links, then splits them up by the pipe
            # character: '|', either a list with two items
            # (left and right of the pipe), or one item (no pipe)
            for link in re.findall(link_regex, wiki_page.find('text').text):
                split_link = str(link).strip().strip("[[]]").strip().split('|')

                # adds left-of-pipe link to list of words to be removed from corpus
                if len(split_link) == 2:
                    self.remove_link_words.extend(
                        split_link[0].lower().replace(":", "").split()) # remove colons from meta links

                # adds link to the ids_links_titles dictionary while 
                # ignoring both duplicate links and links from a page to itself
                if split_link[0] is not wiki_page.find('title').text.strip() and \
                    split_link[0] not in self.ids_links_titles[page_id]:
                        self.ids_links_titles[page_id].append(
                            split_link[0].strip())

            # removes stop words and stems words while filling the
            # words_to_doc_relevance and word_count_in_page dictionaries
            for word in words:
                if word not in STOP_WORDS:  # removes stop words
                    PorterStemmer().stem(word) # stem words
                    if word in self.remove_link_words: # remove left-of-pipe link words
                        self.remove_link_words.remove(word)
                    elif word not in self.words_to_doc_relevance:  # adds to dicts
                        self.words_to_doc_relevance[word] = {page_id: 1}
                        self.word_count_in_page[word] = 1
                    else:  # also populates nested dictionaries
                        if page_id not in self.words_to_doc_relevance[word]:
                            self.words_to_doc_relevance[word][page_id] = 1
                            self.word_count_in_page[word] = 1
                        else:
                            self.words_to_doc_relevance[word][page_id] += 1
                            self.word_count_in_page[word] += 1
            
            # account for empty pages and store the max word count 
            if len(self.word_count_in_page.values()) == 0:
                max_word_count_on_page = 0
            else:
                max_word_count_on_page = max(self.word_count_in_page.values())

            # divides each word count on the current page in the
            # words_to_doc_relevance dictionary by the maximum word count
            # to make words_to_doc_relevance a dictionary of tf values
            for word in self.words_to_doc_relevance:
                if page_id in self.words_to_doc_relevance[word]:
                    self.words_to_doc_relevance[word][page_id] = \
                        self.words_to_doc_relevance[word][page_id] / \
                        max_word_count_on_page

        # use a temporary dictionary to filter out links to titles that aren't found in the corpus
        new_dict = {} # dictionary to be populated with links to titles that are found in the corpus
        for every_id in list(self.ids_links_titles.keys()): # loop through ids
            new_dict[every_id] = [] # build dictionary
            for link in self.ids_links_titles[every_id]: # loop through titles that the id links to
                if link in self.ids_to_titles.values(): # if the linked-to title is in the corpus
                    new_dict[every_id].append(link) # add the linked-to title to the temporary dict
        # store the temporary dict links in the linking-relationships dict
        for id in new_dict:
            self.ids_links_titles[id] = new_dict[id]
                    
    def calc_relevance(self):
        """ Calculate and store relevance values for every word and the pages its found in
        """
        for word in self.words_to_doc_relevance: # loop through every word
            for page in self.words_to_doc_relevance[word]: # loop through every page that a word is found in
                # multiply the previously-stored tf value by the calculated idf value
                self.words_to_doc_relevance[word][page] = self.words_to_doc_relevance[word][page] * math.log(
                    self.TOTAL_DOCS/len(self.words_to_doc_relevance[word]))

    def calc_weight(self):
        """ Calculate and store weights for every link between two ids
        """
        # Precompute and store the weights for when 
        # a page links to nothing and when a page links to itself
        nothing_weight = (self.EPSILON / self.TOTAL_DOCS)\
            + ((1 - self.EPSILON) / (self.TOTAL_DOCS - 1)) # assume that when a page links to nothing, it links to every other page except itself
        otherwise_weight = (self.EPSILON / self.TOTAL_DOCS)

        for k in self.ids_to_titles: # loop through all page ids
            self.weight_dictionary[k] = {}
            for j in self.ids_to_titles: # loop through all page ids
                if len(self.ids_links_titles[k]) == 0 and k != j: # if k links to nothing and the two pages aren't the same
                    self.weight_dictionary[k][j] = nothing_weight
                elif self.ids_to_titles[j] in self.ids_links_titles[k] and k != j: # if j is a page that k links to and the two pages aren't the same
                    self.weight_dictionary[k][j] = (self.EPSILON / self.TOTAL_DOCS)\
                        + ((1 - self.EPSILON) / len(self.ids_links_titles[k]))
                else: # if k and j are the same page
                    self.weight_dictionary[k][j] = otherwise_weight

    def distance(self, old_rankings : dict, new_rankings : dict):
        """ Finds the euclidian distance between two dictionaries
        """
        sum_of_differences = 0
        for rank in new_rankings:
            sum_of_differences += (new_rankings[rank] - old_rankings[rank]) *\
                (new_rankings[rank] - old_rankings[rank])
        return math.sqrt(sum_of_differences)

    def page_rank(self):
        """ Calculate the pageranks for every page
        """
        # initialize rankings r and r'
        self.old_rankings = {id: 0 for id in self.ids_to_titles}
        self.ids_to_pageranks = {id: 1/self.TOTAL_DOCS for id in self.ids_to_titles}

        # ensure distance is below a certain threshold 
        while self.distance(self.old_rankings, self.ids_to_pageranks) > self.DELTA:
            # store the precomputed rankings in the old ranking dict
            for id in self.ids_to_pageranks:
                self.old_rankings[id] = self.ids_to_pageranks[id]
            
            for j in self.ids_to_titles:  # for every page j in the corpus
                self.ids_to_pageranks[j] = 0.0  # initialize the pagerank of the page to 0
                for k in self.ids_to_titles: # for every page k in the corpus
                    self.ids_to_pageranks[j] += (self.weight_dictionary[k][j] *
                                                 self.old_rankings[k]) # pagerank calculation based on weights and old rankings


if __name__ == "__main__":
    """ Main method that ensures the correct number of arguments passed
    and initializes the Indexer with command-line arguments
    """
    if len(sys.argv) < 5: # 5 because we include "index.py"
        print("Fewer than four arguments!")
    else:
        Indexer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]) # pass in xml and the four text files to write to
