from sys import argv
from index import *
from query import *

sys.argv = ["index.py", "wikis/PageRankExample3.xml",
            "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
#print(Indexer().ids_to_titles)
#print(Indexer().links_from_page)
#print(Indexer().words_to_doc_relevance)
#print(Indexer().weight_dictionary)
print(Indexer().ids_to_pageranks)

# sys.argv = ["query.py", "--pagerank", "wikis/PageRankExample3.xml", 
#              "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
# print(Query().ids_to_relevance)