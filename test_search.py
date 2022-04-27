from sys import argv
from index import *
from query import *

sys.argv = ["python3", "index.py", "wikis/PageRankExample3.xml",
             "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
# # print(Index().ids_to_titles)
# # # print(Index().links_from_page)
# # print(Index().words_to_doc_relevance)
print(Indexer("wikis/PageRankExample3.xml",
             "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt").weight_dictionary)
# print(Indexer("wikis/PageRankExample3.xml",
#              "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt").ids_to_pageranks)

sys.argv = ["query.py", "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
# print(Query().ids_to_relevance)
