from posixpath import split
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
               
        self.id_to_title = {}
        self.link_to_links = {}

        if len(sys.argv) - 1 != 4:
            print("Fewer than four arguments!")
        else:
            self.parse(sys.argv[1])
            write_title_file(sys.argv[2], self.id_to_title)
            self.tokenize()

    def parse(self, input_file : String) -> None:
        wiki_tree = et.parse(input_file)
        wiki_xml_root = wiki_tree.getroot()

        for wiki_page in wiki_xml_root:
            self.corpus.add(wiki_page.find('title').text.strip().lower())
            
            self.id_to_title[int(wiki_page.find('id').text.strip())] = wiki_page.find('title').text.strip()
                
            self.corpus.add(wiki_page.find('text').text.strip().lower())
            
    def tokenize(self) -> None:
        self.old_corpus = self.corpus 
        self.corpus = set()
        link_regex = '''\[\[[^\[]+?\]\]'''
        text_regex = '''[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        STOP_WORDS = set(stopwords.words('english'))

        for string in self.old_corpus:
            text = re.findall(text_regex, string)
            links = re.findall(link_regex, string)
            for word in text:
                if word not in STOP_WORDS:
                    stemmer = PorterStemmer(word)
                    self.corpus.add(word)

            for link in links:
                split_link = str(link).split('|')
                if len(split_link) == 1:
                    self.corpus.add(split_link[0])
                    self.link_to_links[split_link[0]] = []
                elif len(split_link) == 2:
                    self.corpus.add(split_link[1])
                    self.link_to_links[split_link[0]] = []
                else:
                    break