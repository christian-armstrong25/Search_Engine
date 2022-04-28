from sys import argv
from index import *
from query import *

sys.argv = ["python3", "index.py", "wikis/HandoutWiki.xml",
             "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
# Indexer("wikis/MedWiki.xml", "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt")
# # print(Indexer().ids_to_titles)
# print(Indexer("wikis/HandoutWiki.xml",
#               "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt").ids_links_titles)
print(Indexer("wikis/HandoutWiki.xml",
            "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt").words_to_doc_relevance)
# print(Indexer("wikis/MedWiki.xml",
#              "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt").weight_dictionary)
# print(Indexer("wikis/MedWiki.xml",
#              "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt").ids_to_pageranks)

# sys.argv = ["query.py", "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
# print(Querier(True, "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt").words_to_doc_relevance)

