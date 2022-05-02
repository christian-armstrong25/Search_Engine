from sys import argv
from index import *
from query import *

# sys.argv = ["python3", "index.py", "wikis/MedWiki.xml",
#              "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
# Indexer("wikis/MedWiki.xml", "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt")
# # print(Indexer().ids_to_titles)
# print(Indexer("wikis/SmallWiki.xml",
#               "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt").ids_links_titles)
print(Indexer("wikis/HandoutWiki.xml",
            "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt").words_to_doc_relevance)
# print(Indexer("wikis/MedWiki.xml",
#              "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt").weight_dictionary)
# print(Indexer("wikis/MedWiki.xml",
#              "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt").ids_to_pageranks)

# sys.argv = ["query.py", "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt"]
# Querier("--pagerank", "text_files/titles.txt", "text_files/docs.txt", "text_files/words.txt")

def test_relevance1():
    assert Indexer("wikis/HandoutWiki.xml",
            "text_files/titles.txt", "text_files/docs.txt", 
            "text_files/words.txt").words_to_doc_relevance == \
                {'dog': {1: 0.4054651081081644, 2: 0.4054651081081644}, 
                'bit': {1: 0.4054651081081644, 3: 0.2027325540540822}, 
                'man': {1: 1.0986122886681098}, 'ate': {2: 1.0986122886681098}, 
                'cheese': {2: 0.4054651081081644, 3: 0.4054651081081644}, 
                'b': {2: 1.0986122886681098}, 'c': {3: 0.5493061443340549}}