from msilib.schema import File
import sys
import xml.etree.ElementTree as et

class Indexer:
    def __init__(self) -> None:
        pass

    def parse(input_file : String) -> None:
        wiki_tree = et.parse(input_file)
        wiki_xml_root = wiki_tree.getroot()
        for wiki_page in wiki_xml_root:
            
