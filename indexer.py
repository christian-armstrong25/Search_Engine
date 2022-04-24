import sys
from tokenize import String
import xml.etree.ElementTree as et
import re
from file_io import write_title_file
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


class Indexer:
    def __init__(self) -> None:
        self.corpus = set()

        self.ids_to_titles = {}
        self.link_to_title = {}
        self.words_to_doc_relevance = {}

        if len(sys.argv) - 1 != 4:
            print("Fewer than four arguments!")
        else:
            self.parse(sys.argv[1])
            write_title_file(sys.argv[2], self.ids_to_titles)

    def parse(self, input_file: String) -> None:
        link_regex = '''\[\[[^\[]+?\]\]'''
        text_regex = '''[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        STOP_WORDS = set(stopwords.words('english'))
        stemmer = PorterStemmer()
        wiki_tree = et.parse(input_file)
        wiki_xml_root = wiki_tree.getroot()

        for wiki_page in wiki_xml_root:
            page_id = int(wiki_page.find('id').text.strip())
            self.word_count_in_page = {}
            self.ids_to_titles[page_id] = wiki_page.find('title').text.strip()
            words = [re.findall(text_regex, wiki_page.find(
                'text').text.strip().lower())]
            words.append(re.findall(text_regex, wiki_page.find(
                'title').text.strip().lower()))

            for link in re.findall(link_regex, wiki_page.find('text').text):
                split_link = str(link).strip().strip("[[]]").strip().split('|')

                if len(split_link) == 1:
                    words.append(split_link[0])
                else:
                    words.append(split_link[1])

                if split_link[0] in self.link_to_title:
                    list(self.link_to_title[split_link[0]]).append(
                        wiki_page.find('title').text.strip())
                else:
                    self.link_to_title[split_link[0]] = [
                        wiki_page.find('title').text.strip()]

            for word in words:
                if word not in STOP_WORDS:
                    self.corpus.add(stemmer.stem(word))
                    if word not in self.words_to_doc_relevance:
                        self.words_to_doc_relevance[word] = {page_id: 1}
                        self.word_count_in_page[word] = 1
                    else:
                        if int(wiki_page.find('id').text.strip()) not in self.words_to_doc_relevance[word]:
                            self.words_to_doc_relevance[word][page_id] = 1
                            self.word_count_in_page[word] = 1
                        else:
                            self.words_to_doc_relevance[word][page_id] += 1
                            self.word_count_in_page[word] += 1

            word_counts = self.word_count_in_page.values()
            max_word_count_on_page = max(word_counts)

            for word in self.words_to_doc_relevance:
                if page_id in self.words_to_doc_relevance[word]:
                    self.words_to_doc_relevance[word][page_id] /= max_word_count_on_page
