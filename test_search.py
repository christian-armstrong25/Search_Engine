from sys import argv
from indexer import *
from query import *

sys.argv = ["indexer.py", "wikis/HandoutWiki.xml",
            "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
#print(Indexer().corpus)
#print(Indexer().ids_to_titles)
#print(Indexer().links_from_page)
#print(Indexer().words_to_doc_relevance)
print(Indexer().ids_to_pageranks)
