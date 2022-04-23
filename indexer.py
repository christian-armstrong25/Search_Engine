from msilib.schema import File
import sys
import xml.etree.ElementTree as et

class Indexer:
    def __init__(self) -> None:
        pass

    def parse(input_file : String) -> :
        wiki_tree = et.parse(input_file)
        wiki_xml_root = wiki_tree.getroot()

        text_set = set()
        for wiki_page in wiki_xml_root:
            title = wiki_page.find('title').text.strip()
            if title not in text_set:
                text_set.add(title)
            
            id = int(wiki_page.find('id').text.strip())
            if id not in text_set:
                text_set.add(id)

            text = wiki_page.find('text').text.strip()
            if text not in text_set:
                text_set.add(text)
        
