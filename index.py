from copy import copy
from ipaddress import summarize_address_range
from optparse import TitledHelpFormatter
import sys
from tokenize import String
from warnings import catch_warnings
import xml.etree.ElementTree as et
import re
from file_io import write_docs_file, write_title_file, write_words_file
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import math
STOP_WORDS = set(stopwords.words('english'))


class Indexer:
    def __init__(self, xml, titles, docs, words) -> None:
        self.ids_to_titles = {}  # maps page ids to page titles
        self.ids_links_titles = {}  # maps an id to all the titles it links to
        self.ids_to_pageranks = {}  # maps ids to pageranks
        # double dictionary from words, to the documents they appear in, to
        # the relevance of those documents to that word according to tf and idf
        self.words_to_doc_relevance = {}
        self.EPSILON = 0.15
        self.DELTA = 0.001
        self.parse(xml)  # parses the XML file
        self.TOTAL_DOCS = len(self.ids_to_titles)
        self.calc_relevance()
        # double dictionary of ids to ids to weights
        self.weight_dictionary = {}
        self.calc_weight()
        self.page_rank()
        self.sum = sum(self.ids_to_pageranks.values())
        # writes to the title file
        write_title_file(titles, self.ids_to_titles)
        # writes to the docs file
        write_docs_file(docs, self.ids_to_pageranks)
        # writes to the words file
        write_words_file(words, self.words_to_doc_relevance)

    def parse(self, input_file: String) -> None:
        link_regex = '''\[\[[^\[]+?\]\]'''
        text_regex = '''[a-zA-Z]+'[a-zA-Z]+|[a-zA-Z]+'''
        wiki_tree = et.parse(input_file)  # parses the XML file
        wiki_xml_root = wiki_tree.getroot()

        for wiki_page in wiki_xml_root:
            # id of current page
            page_id = int(wiki_page.find('id').text.strip())

            # dictionary from word to count on current page
            self.word_count_in_page = {}

            # list of all words in current page
            words = []

            # adds the current id and title pair to the ids_to_titles dictionary
            self.ids_to_titles[page_id] = wiki_page.find(
                'title').text.strip()

            # tokenized words
            words.extend(re.findall(text_regex, wiki_page.find(
                'text').text.strip().lower()))  # appends on words from texts
            words.extend(re.findall(text_regex, wiki_page.find(
                'title').text.strip().lower()))  # appends on words from titles

            self.ids_links_titles[page_id] = []
            self.remove_link_words = []
            # removes brackets from links, then splits them up by the pipe
            # character: '|', either a list with two items
            # (left and right of the pipe), or one item (no pipe)
            for link in re.findall(link_regex, wiki_page.find('text').text):
                split_link = str(link).strip().strip("[[]]").strip().split('|')

                # adds pipe link to be removed from words
                if len(split_link) == 2:
                    self.remove_link_words.extend(
                        split_link[0].lower().replace(":", "").split())

                # adds link to the ids_links_titles dictionary
                # ignores links from a page to itself
                if split_link[0] is not wiki_page.find('title').text.strip() and split_link[0] not in self.ids_links_titles[page_id]:
                    self.ids_links_titles[page_id].append(
                        split_link[0].strip())

            # removes stop words and stems words while filling the
            # words_to_doc_relevance and word_count_in_page dictionaries
            for word in words:
                if word not in STOP_WORDS:  # removes stop words
                    PorterStemmer().stem(word)
                    if word in self.remove_link_words:
                        self.remove_link_words.remove(word)
                    elif word not in self.words_to_doc_relevance:  # adds to dicts
                        self.words_to_doc_relevance[word] = {page_id: 1}
                        self.word_count_in_page[word] = 1
                    else:  # also populates dictionaries
                        if page_id not in self.words_to_doc_relevance[word]:
                            self.words_to_doc_relevance[word][page_id] = 1
                            self.word_count_in_page[word] = 1
                        else:
                            self.words_to_doc_relevance[word][page_id] += 1
                            self.word_count_in_page[word] += 1

            # # the maximum count of all the words in the page
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

        for id in self.ids_links_titles:
            for element in self.ids_links_titles[id]:
                print(element)
                if element not in self.ids_to_titles.values():
                    self.ids_links_titles[id].remove(element)
        print(self.ids_links_titles)

    def calc_relevance(self):
        # multiplies each tf value in the words_to_doc_relevance dictionary by
        # the idf score of the word the tf value is calculated from, turning
        # the values in the words_to_doc_relevance into relevance values
        # the total number of pages in the given XML
        for word in self.words_to_doc_relevance:
            for page in self.words_to_doc_relevance[word]:
                self.words_to_doc_relevance[word][page] = self.words_to_doc_relevance[word][page] * math.log(
                    self.TOTAL_DOCS/len(self.words_to_doc_relevance[word]))

    def calc_weight(self):
        nothing_weight = (self.EPSILON / self.TOTAL_DOCS)\
            + ((1 - self.EPSILON) / (self.TOTAL_DOCS - 1))
        otherwise_weight = (self.EPSILON / self.TOTAL_DOCS)
        for k in self.ids_to_titles:
            self.weight_dictionary[k] = {}
            print(self.ids_links_titles[k])
            for j in self.ids_to_titles:
                if len(self.ids_links_titles[k]) == 0 and k != j:
                    self.weight_dictionary[k][j] = nothing_weight
                elif self.ids_to_titles[j] in self.ids_links_titles[k] and k != j:
                    self.weight_dictionary[k][j] = (self.EPSILON / self.TOTAL_DOCS)\
                        + ((1 - self.EPSILON) / len(self.ids_links_titles[k]))
                else:
                    self.weight_dictionary[k][j] = otherwise_weight
            print(sum(self.weight_dictionary[k].values()))

    # finds the euclidian distance between two dictionaries
    def distance(self, old_rankings, new_rankings):
        sum_of_differences = 0
        for rank in new_rankings:
            sum_of_differences += (new_rankings[rank] - old_rankings[rank]) *\
                (new_rankings[rank] - old_rankings[rank])
        return math.sqrt(sum_of_differences)

    def page_rank(self):
        # initialize rankings (r and r')
        # self.old_rankings = self.ids_to_titles.copy()
        self.old_rankings = {id: 0 for id in self.ids_to_titles}  # r
        self.ids_to_pageranks = {
            id: 1/self.TOTAL_DOCS for id in self.ids_to_titles}  # r'
        # for ids in self.ids_to_pageranks:
        #     # initialize every rank in r to be 0
        #     self.old_rankings[ids] = 0
        #     # initialize every rank in r' to be 1/n
        #     self.ids_to_pageranks[ids] = 1/self.TOTAL_DOCS

        while self.distance(self.old_rankings, self.ids_to_pageranks) > self.DELTA:
            for id in self.ids_to_pageranks:
                self.old_rankings[id] = self.ids_to_pageranks[id]  # r <- r'
            for j in self.ids_to_titles:  # for j in pages
                self.ids_to_pageranks[j] = 0.0  # r'(j) = 0
                # for k in pages
                for k in self.ids_to_titles:
                    # r'(j) = r'(j) + weight(k, j) * r(k)
                    self.ids_to_pageranks[j] += (self.weight_dictionary[k][j] *
                                                 self.old_rankings[k])

if __name__ == "__main__":
    sys.argv = ["index.py", "wikis/SmallWiki2.xml", "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
    if len(sys.argv) < 5:
        print("Fewer than four arguments!")
    else:
        Indexer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        # Indexer("wikis/SmallWiki2.xml",
        #     "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt")
