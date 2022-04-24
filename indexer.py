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

    def parse(self, input_file : String) -> None:
        link_regex = '''\[\[[^\[]+?\]\]'''
        text_regex = '''[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        STOP_WORDS = set(stopwords.words('english'))
        stemmer = PorterStemmer()
        wiki_tree = et.parse(input_file)
        wiki_xml_root = wiki_tree.getroot()

        for wiki_page in wiki_xml_root:
            for title_word in re.findall(text_regex, wiki_page.find('title').text.strip().lower()):
                if title_word not in STOP_WORDS:
                    self.corpus.add(stemmer.stem(title_word))
            
            self.ids_to_titles[int(wiki_page.find('id').text.strip())] = wiki_page.find('title').text.strip().lower()
                
            for text_word in re.findall(text_regex, wiki_page.find('text').text.strip().lower()):
                if text_word not in STOP_WORDS:
                    self.corpus.add(stemmer.stem(text_word))

            for link in re.findall(link_regex, wiki_page.find('text').text):
                split_link = str(link).strip().strip("[[]]").strip().split('|')
                if len(split_link) == 1:
                    self.corpus.add(split_link[0])
                    if split_link[0] in self.link_to_title:
                        list(self.link_to_title[split_link[0]]).append(wiki_page.find('title').text.strip())
                    else:
                        self.link_to_title[split_link[0]] = [wiki_page.find('title').text.strip()]
                elif len(split_link) == 2:
                    self.corpus.add(split_link[1])
                    if split_link[0] in self.link_to_title:
                        list(self.link_to_title[split_link[0]]).append(wiki_page.find('title').text.strip())
                    else:
                        self.link_to_title[split_link[0]] = [wiki_page.find('title').text.strip()]
                else:
                    break
    
    def term_frequency(self, input_file : String):
        
