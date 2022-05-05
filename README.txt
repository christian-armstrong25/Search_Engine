Group members: Christian Armstrong, Daniel Liu

Known bugs: None

Instructions for use: 

The user would first run the Indexer by typing into the terminal: 
index.py <XML filepath> <titles filepath> <docs filepath> <words filepath>

Where 
<XML filepath> is the file path of the XML you want to search for pages from, 

<titles filepath> is the file path of the text file you would like to write ID-Title pairings to, 

<docs filepath> is the file path of the text file you would like to write ID-Pagerank pairings, and 

<words filepath> is the file path of the text file you would like to write Word-ID-Relevance pairings. 


Next the user would run the Querier to begin searching for pages from those processed by the Indexer by typing into the terminal:
query.py [--pagerank] <titleIndex> <documentIndex> <wordIndex>

Where 
[--pagerank] is an optional argument specifying whether the you want your search results to consider the pagerank of a page when ranking search results

<titleIndex> is the file path of the text file you wrote ID-Title pairings to in the Indexer

<documentIndex> is the file path of the text file you wrote ID-Pagerank pairings to in the Indexer, and 

<wordIndex> is the file path of the text file you wrote Word-ID-Relevance pairings to in the Indexer.


Finally, the user will be promoted to search for pages, and should type strings into the terminal to do so. To end the program, a user must type ":quit" into the 


How the pieces of our program fit together:

Our Indexer initializes the following three dictionaries: ids_to_titles, ids_links_titles, ids_to_pageranks. Our Indexer then begins to parse. For each page, we record the ID and Title, then put that pairing into ids_to_titles. In the same loop for each page we record the ID of the current page and the titles of any pages it links to by using a regex that finds links and a conditional statement to take the part that is a link if it is not a link to the current page and is not a link to a page that the current page has already linked to. We record these ID to list of tittles it links to in ids_links_titles. Also in the same for loop, we add all the words from the title and text of a page into a list of words which we loop through to stem 