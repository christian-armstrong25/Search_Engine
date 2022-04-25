from ipaddress import summarize_address_range
import sys
from tokenize import String
from turtle import title
import xml.etree.ElementTree as et
import re
from file_io import write_docs_file, write_title_file, write_words_file
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import math
STOP_WORDS = set(stopwords.words('english'))


class Indexer:
    def __init__(self) -> None:
        self.corpus = set()  # set of all words in the given XML file
        self.ids_to_titles = {}  # maps page ids to page titles
        self.links_from_page = {}  # maps an id to all the titles it links to
        self.ids_to_pageranks = {}  # maps ids to pageranks

        # double dictionary from words, to the documents they appear in, to
        # the relevance of those documents to that word according to tf and idf
        self.words_to_doc_relevance = {}
        self.EPSILON = 0.15
        self.DELTA = 0.001
        # prints message if less than 4 arguments in terminal
        if len(sys.argv) - 1 != 4:
            print("Fewer than four arguments!")
        else:
            self.parse(sys.argv[1])  # parses the XML file
            self.calc_relevance()
            # double dictionary of ids to ids to weights
            self.weight_dictionary = self.ids_to_titles.copy()
            self.calc_weight()
            self.page_rank()
            # writes to the title file
            write_title_file(sys.argv[2], self.ids_to_titles)
            # writes to the words file
            write_words_file(sys.argv[4], self.words_to_doc_relevance)
            # writes to the docs file
            write_docs_file(sys.argv[3], self.ids_to_pageranks)

    def parse(self, input_file: String) -> None:
        link_regex = '''\[\[[^\[]+?\]\]'''
        text_regex = '''[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        stemmer = PorterStemmer()
        wiki_tree = et.parse(input_file)  # parses the XML file
        wiki_xml_root = wiki_tree.getroot()

        for wiki_page in wiki_xml_root:
            # id of current page
            page_id = int(wiki_page.find('id').text.strip())

            # dictionary from word to count on current page
            self.word_count_in_page = {}

            # adds the current id and title pair to the ids_to_titles dictionary
            self.ids_to_titles[page_id] = wiki_page.find(
                'title').text.strip()

            # tokenized words
            words = set()
            words.update(re.findall(text_regex, wiki_page.find(
                'text').text.strip().lower()))  # appends on words from texts
            words.update(re.findall(text_regex, wiki_page.find(
                'title').text.strip().lower()))  # appends on words from titles

            # removes brackets from links, then splits them up by the pipe
            # character: '|', either a list with two items
            # (left and right of the pipe), or one item (no pipe)
            for link in re.findall(link_regex, wiki_page.find('text').text):
                split_link = str(link).strip().strip("[[]]").strip().split('|')

                # appends the text from a link to words
                if len(split_link) == 1:
                    words.update(split_link[0].strip(
                        ":").replace(":", "").split())
                else:
                    words.update(split_link[1].strip(
                        ":").replace(":", "").split())

                # adds link to the links_from_page dictionary
                if page_id in self.links_from_page:
                    # ignores links from a page to itself
                    if split_link[0] != wiki_page.find('title').text.strip():
                        set(self.links_from_page[page_id]).add(split_link[0])
                else:
                    # set only contains unique links
                    self.links_from_page[page_id] = set(split_link[0])

            # removes stop words and stems words while filling the
            # words_to_doc_relevance and word_count_in_page dictionaries
            for word in words:
                if word not in STOP_WORDS:  # removes stop words
                    self.corpus.add(stemmer.stem(word))  # stems words
                    if word not in self.words_to_doc_relevance:  # adds to dicts
                        self.words_to_doc_relevance[word] = {page_id: 1}
                        self.word_count_in_page[word] = 1
                    else:  # also populates dictionaries
                        if int(wiki_page.find('id').text.strip()) \
                                not in self.words_to_doc_relevance[word]:
                            self.words_to_doc_relevance[word][page_id] = 1
                            self.word_count_in_page[word] = 1
                        else:
                            self.words_to_doc_relevance[word][page_id] += 1
                            self.word_count_in_page[word] += 1

            # an integer list of the count of each word in the page
            word_counts = self.word_count_in_page.values()
            # the maximum count of all the words in the page
            max_word_count_on_page = max(word_counts)

            # divides each word count on the current page in the
            # words_to_doc_relevance dictionary by the maximum word count
            # to make words_to_doc_relevance a dictionary of tf values
            for word in self.words_to_doc_relevance:
                if page_id in self.words_to_doc_relevance[word]:
                    self.words_to_doc_relevance[word][page_id] /= \
                        max_word_count_on_page

    def calc_relevance(self):
        # multiplies each tf value in the words_to_doc_relevance dictionary by
        # the idf score of the word the tf value is calculated from, turning
        # the values in the words_to_doc_relevance into relevance values
        # the total number of pages in the given XML
        self.total_docs = len(self.ids_to_titles)
        for word in self.words_to_doc_relevance:
            for page in self.words_to_doc_relevance[word]:
                self.words_to_doc_relevance[word][page] *= math.log(
                    self.total_docs/len(self.words_to_doc_relevance[word]))

    def calc_weight(self):
        # computes weights and fills weight_dictionary
        for page in self.ids_to_titles:
            self.weight_dictionary[page] = {}
            for link in self.ids_to_titles:
                if page not in self.links_from_page:  # page links to nothing
                    self.weight_dictionary[page][link] = (1 / self.total_docs)
                elif link in self.links_from_page[page]:  # if k links to j
                    self.weight_dictionary[page][link] = (self.EPSILON / self.total_docs)\
                        + ((1 - self.EPSILON) *
                           (1 / len(self.links_from_page[page])))
                else:  # otherwise
                    self.weight_dictionary[page][link] = (
                        self.EPSILON / self.total_docs)

    # finds the euclidian distance between two dictionaries
    def distance(self, old_rankings, new_rankings):
        sum_of_differences = 0
        for rank in new_rankings:
            sum_of_differences += (new_rankings[rank] - old_rankings[rank]) *\
                (new_rankings[rank] - old_rankings[rank])
        return math.sqrt(sum_of_differences)

    def page_rank(self):
        # initialize rankings (r and r')
        self.old_rankings = self.ids_to_titles.copy()  # r
        self.ids_to_pageranks = self.ids_to_titles.copy()  # r'
        for ids in self.ids_to_pageranks:
            # initialize every rank in r to be 0
            self.old_rankings[ids] = 0
            # initialize every rank in r' to be 1/n
            self.ids_to_pageranks[ids] = 1/self.total_docs

        # computes PageRank using weight_dictionary and two ranking
        # dictionaries: old_rankings (r) and ids_to_pageranks (r')
        for pages in self.ids_to_pageranks:
            # while distance(r, r') > delta:
            while self.distance(self.old_rankings, self.ids_to_pageranks) > self.DELTA:
                self.old_rankings = self.ids_to_pageranks.copy()  # r <- r'
                for pages in self.weight_dictionary:  # for j in pages
                    new_rank = 0  # r'(j) = 0
                    # for k in pages
                    for link in self.weight_dictionary[pages]:
                        # r'(j) = r'(j) + weight(k, j) * r(k)
                        new_rank += self.weight_dictionary[pages][link] *\
                            self.old_rankings[link]
                    self.ids_to_pageranks[pages] = new_rank
