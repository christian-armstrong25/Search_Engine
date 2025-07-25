from sys import argv
from index import *
from query import *

def test_relevance_handout():
    assert Indexer("wikis/HandoutWiki.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").words_to_doc_relevance == \
        {'dog': {1: 0.4054651081081644, 2: 0.4054651081081644},
         'bit': {1: 0.4054651081081644, 3: 0.2027325540540822},
         'man': {1: 1.0986122886681098}, 'ate': {2: 1.0986122886681098},
         'cheese': {2: 0.4054651081081644, 3: 0.4054651081081644},
         'b': {2: 1.0986122886681098}, 'c': {3: 0.5493061443340549}}


def test_relevance_from_conceptual_check():
    assert Indexer("wikis/HandoutWiki2.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").words_to_doc_relevance == \
        {'signing': {0: 1.3862943611198906},
         'contract': {0: 0.6931471805599453, 1: 0.6931471805599453},
         'creates': {0: 1.3862943611198906}, 'contractual': {0: 1.3862943611198906},
         'obligation': {0: 1.3862943611198906},
         'cold': {1: 0.14384103622589042, 2: 0.28768207245178085, 3: 0.28768207245178085},
         'flu': {1: 0.6931471805599453}, 'b': {1: 0.6931471805599453},
         'water': {2: 0.6931471805599453, 3: 0.6931471805599453},
         'signs': {2: 1.3862943611198906}, 'likely': {2: 1.3862943611198906},
         'get': {2: 1.3862943611198906}, 'c': {2: 1.3862943611198906}}


def test_weights_from_conceptual_check():
    assert Indexer("wikis/HandoutWiki3.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").weight_dictionary == \
        {1: {1: 0.0375, 2: 0.46249999999999997, 3: 0.0375, 4: 0.46249999999999997},
         2: {1: 0.0375, 2: 0.0375, 3: 0.46249999999999997, 4: 0.46249999999999997},
         3: {1: 0.3208333333333333, 2: 0.3208333333333333, 3: 0.0375, 4: 0.3208333333333333},
         4: {1: 0.46249999999999997, 2: 0.0375, 3: 0.46249999999999997, 4: 0.0375}}


def test_pagerank_from_conceptual_check():
    assert Indexer("wikis/HandoutWiki3.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").ids_to_pageranks == \
        {1: 0.23667466796061043, 2: 0.21018172650775616,
         3: 0.25380079601405847, 4: 0.29934280951757436}


def test_pagerank_example1():
    assert Indexer("wikis/PageRankExample1.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").ids_to_pageranks == \
        {1: 0.4326427188659158, 2: 0.23402394780075067, 3: 0.33333333333333326}


def test_pagerank_example2():
    assert Indexer("wikis/PageRankExample2.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").ids_to_pageranks == \
        {1: 0.20184346250214996, 2: 0.03749999999999998,
         3: 0.37396603749279056, 4: 0.3866905000050588}


def test_pagerank_example3():
    assert Indexer("wikis/PageRankExample3.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").ids_to_pageranks == \
        {1: 0.05242784862611451, 2: 0.05242784862611451,
         3: 0.4475721513738852, 4: 0.44757215137388523}


def test_pagerank_example4():
    assert Indexer("wikis/PageRankExample4.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").ids_to_pageranks == \
        {1: 0.0375, 2: 0.0375, 3: 0.46249999999999997, 4: 0.4624999999999999}


def test_weights_no_links():
    assert Indexer("wikis/CustomWiki1.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").weight_dictionary == \
        {1: {1: 0.049999999999999996, 2: 0.475, 3: 0.475},
         2: {1: 0.475, 2: 0.049999999999999996, 3: 0.475},
         3: {1: 0.475, 2: 0.475, 3: 0.049999999999999996}}


def test_pagerank_no_links():
    assert Indexer("wikis/CustomWiki1.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").ids_to_pageranks == \
        {1: 0.3333333333333333, 2: 0.3333333333333333, 3: 0.3333333333333333}


def test_weights_all_self_links():
    assert Indexer("wikis/CustomWiki2.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").weight_dictionary == \
        {1: {1: 0.049999999999999996, 2: 0.475, 3: 0.475},
         2: {1: 0.475, 2: 0.049999999999999996, 3: 0.475},
         3: {1: 0.475, 2: 0.475, 3: 0.049999999999999996}}


def test_pagerank_all_self_links():
    assert Indexer("wikis/CustomWiki2.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").ids_to_pageranks == \
        {1: 0.3333333333333333, 2: 0.3333333333333333, 3: 0.3333333333333333}


def test_weights_duplicate_links():
    assert Indexer("wikis/CustomWiki3.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").weight_dictionary == \
        {1: {1: 0.049999999999999996, 2: 0.049999999999999996, 3: 0.9},
         2: {1: 0.9, 2: 0.049999999999999996, 3: 0.049999999999999996},
         3: {1: 0.049999999999999996, 2: 0.9, 3: 0.049999999999999996}}


def test_pagerank_duplicate_links():
    assert Indexer("wikis/CustomWiki3.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").ids_to_pageranks == \
        {1: 0.3333333333333333, 2: 0.3333333333333333, 3: 0.3333333333333333}


def test_weights_all_nonexistent_links():
    assert Indexer("wikis/CustomWiki4.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").weight_dictionary == \
        {1: {1: 0.049999999999999996, 2: 0.475, 3: 0.475},
         2: {1: 0.475, 2: 0.049999999999999996, 3: 0.475},
         3: {1: 0.475, 2: 0.475, 3: 0.049999999999999996}}


def test_pagerank_all_nonexistent_links():
    assert Indexer("wikis/CustomWiki4.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").ids_to_pageranks == \
        {1: 0.3333333333333333, 2: 0.3333333333333333, 3: 0.3333333333333333}


def test_distance_basic():
    old_rankings = {
        1: .3333,
        2: .3333,
        3: .3333
    }
    new_rankings = {
        1: .4750,
        2: .1916,
        3: .3333
    }
    assert Indexer("wikis/CustomWiki4.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").distance(old_rankings, new_rankings) < \
        .2004 and Indexer("wikis/CustomWiki4.xml",
                          "text_files/titles.txt", "text_files/docs.txt",
                          "text_files/words.txt").distance(old_rankings, new_rankings) > \
        .2002


def test_distance_advanced():
    old_rankings = {
        1: .4330,
        2: .2337,
        3: .3333
    }
    new_rankings = {
        1: .4326,
        2: .2340,
        3: .3333
    }
    assert Indexer("wikis/CustomWiki4.xml",
                   "text_files/titles.txt", "text_files/docs.txt",
                   "text_files/words.txt").distance(old_rankings, new_rankings) < \
        .0006 and Indexer("wikis/CustomWiki4.xml",
                          "text_files/titles.txt", "text_files/docs.txt",
                          "text_files/words.txt").distance(old_rankings, new_rankings) > \
        .0004

def test_links():
    assert Indexer("wikis/PageRankExample1.xml",
              "text_files/titles.txt", "text_files/docs.txt", 
              "text_files/words.txt").ids_links_titles == \
                {1: ['B', 'C'], 2: [], 3: ['A']}

def test_links2():
    assert Indexer("wikis/HandoutWiki3.xml",
              "text_files/titles.txt", "text_files/docs.txt",
              "text_files/words.txt").ids_links_titles == \
                {1: ['B', 'D'], 2: ['C', 'D'], 3: [], 4: ['A', 'C']}