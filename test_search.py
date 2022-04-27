from sys import argv
from index import *
from query import *

sys.argv = ["index.py", "wikis/SmallWiki.xml",
            "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
# print(Index().ids_to_titles)
# print(Index().links_from_page)
# print(Index().words_to_doc_relevance)
# # print(Index().weight_dictionary)
# print(Index().ids_to_pageranks)

sys.argv = ["query.py", "--pagerank", "wikis/SmallWiki.xml",
             "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
print(Query().ids_to_relevance)
