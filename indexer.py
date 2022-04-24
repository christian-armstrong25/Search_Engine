import sys
from tokenize import String
from turtle import title
import xml.etree.ElementTree as et
import re
from file_io import write_title_file, write_words_file
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import math


class Indexer:
    def __init__(self) -> None:
        self.corpus = set()  # set of all words in the given XML file
        self.ids_to_titles = {}  # maps page ids to page titles
        self.links_from_page = {}  # maps an id to all the titles it links to
        self.ids_to_pageranks = {}  # maps ids to pageranks

        # double dictionary from words, to the documents they appear in, to
        # the relevance of those documents to that word according to tf and idf
        self.words_to_doc_relevance = {}

        # prints message if less than 4 arguments in terminal
        if len(sys.argv) - 1 != 4:
            print("Fewer than four arguments!")
        else:
            self.parse(sys.argv[1])  # parses the XML file

            # writes to the title file
            write_title_file(sys.argv[2], self.ids_to_titles)
            # writes to the words file
            write_words_file(self.words_to_doc_relevance, sys.argv[4])

    def parse(self, input_file: String) -> None:
        link_regex = '''\[\[[^\[]+?\]\]'''
        text_regex = '''[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        STOP_WORDS = set(stopwords.words('english'))
        stemmer = PorterStemmer()
        wiki_tree = et.parse(input_file)  # parses the XML file
        wiki_xml_root = wiki_tree.getroot()

        for wiki_page in wiki_xml_root:
            # id of current page
            page_id = int(wiki_page.find('id').text.strip())

            # dictionary from word to count on current page
            self.word_count_in_page = {}

            # adds the current id and title pair to the ids_to_titles dictionary
            self.ids_to_titles[page_id] = wiki_page.find('title').text.strip()

            # tokenized words
            words = []
            words.append(re.findall(text_regex, wiki_page.find(
                'text').text.strip().lower()))  # appends on words from texts
            words.append(re.findall(text_regex, wiki_page.find(
                'title').text.strip().lower()))  # appends on words from titles

            # removes brackets from links, then splits them up by the pipe
            # character: '|', either a list with two items
            # (left and right of the pipe), or one item (no pipe)
            for link in re.findall(link_regex, wiki_page.find('text').text):
                split_link = str(link).strip().strip("[[]]").strip().split('|')

                # appends the text from a link to words
                if len(split_link) == 1:
                    words.append(split_link[0])
                else:
                    words.append(split_link[1])

                # adds link to the link_to_title dictionary
                if page_id in self.links_to_id:
                    # ignores links from a page to itself
                    if split_link[link] != wiki_page.find('title').text.strip():
                        self.links_from_page[page_id].add(split_link[0])
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

        # the total number of pages in the given XML
        total_docs = len(self.ids_to_titles)

        # multiplies each tf value in the words_to_doc_relevance dictionary by
        # the idf score of the word the tf value is calculated from, turning
        # the values in the words_to_doc_relevance into relevance values
        for word in self.words_to_doc_relevance:
            for page in self.words_to_doc_relevance[word]:
                self.words_to_doc_relevance[word][page] *= math.log(
                    total_docs/len(self.words_to_doc_relevance[word]))

        epsilon = 0.15
        self.ids_to_pageranks = self.ids_to_titles

        for page in self.ids_to_titles:
            self.ids_to_pageranks[page] = {}
            for link in self.ids_to_titles:
                if page not in self.links_from_page:  # page links to nothing
                    self.ids_to_pageranks[page][link] = (1 / total_docs)
                elif link in self.links_from_page[page]:  # if k links to j
                    self.ids_to_pageranks[page][link] = (epsilon / total_docs) +\
                        ((1 - epsilon) * (1 / len(self.links_to_id[page])))
                else:  # otherwise
                    self.ids_to_pageranks[page][link] = (
                        epsilon / total_docs)
