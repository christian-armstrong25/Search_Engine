from sys import argv
from indexer import *
from query import *

print(1)
sys.argv = ["indexer.py", "wikis/SmallWiki.xml", "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
print(Indexer().corpus)


