from sys import argv
from indexer import *
from query import *

sys.argv = ["indexer.py", "wikis/CustomWiki.xml", "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
print(Indexer().corpus)
print(Indexer().id_to_title)

