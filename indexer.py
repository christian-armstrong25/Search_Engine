import sys
from tokenize import String
from typing import Set
import xml.etree.ElementTree as et

class Indexer:
    def __init__(self) -> None:
        if len(sys.argv) - 1 != 4:
            print("Fewer than four arguments!")
        else:
            self.text_set = set()
            self.parse(sys.argv[1])

    def parse(self, input_file : String) -> None:
        wiki_tree = et.parse(input_file)
        wiki_xml_root = wiki_tree.getroot()

        for wiki_page in wiki_xml_root:
            self.text_set.add(wiki_page.find('title').text.strip())
            
            self.text_set.add(int(wiki_page.find('id').text.strip()))

            self.text_set.add(wiki_page.find('text').text.strip())
            
    def tokenize(self, text_set : Set) -> None:
        link_regex = '''\[\[[^\[]+?\]\]'''
        text_regex = '''[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''

        for 
        cool_token = re.findall(n_regex, "this is a cool string")


        
    
