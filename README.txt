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

where 
[--pagerank] is an optional argument specifying whether the you want your search results to consider the pagerank of a page when ranking search results
<titleIndex> is the file path of the text file you wrote ID-Title pairings to in the Indexer
<documentIndex> is the file path of the text file you wrote ID-Pagerank pairings to in the Indexer, and 
<wordIndex> is the file path of the text file you wrote Word-ID-Relevance pairings to in the Indexer.

Finally, the user will be promoted to search for pages, and should type strings into the terminal to do so. To end the program, a user must type ":quit" into the terminal.

How the pieces of our program fit together:

Our Indexer initializes the following three dictionaries: ids_to_titles, ids_links_titles, ids_to_pageranks. Our Indexer then begins to parse. 
For each page, we record the ID and Title, then put that pairing into ids_to_titles. In the same loop for each page we record the ID of the 
current page and the titles of any pages it links to by using a regex that finds links and a conditional statement to take the part that is a 
link if it is not a link to the current page and is not a link to a page that the current page has already linked to. We record these ID to 
list of titles it links to in ids_links_titles. Also in the same for loop, we add all the words from the title and text of a page into a 
list of words which we loop through to stem and remove stop words while also storing the count of each word on each page that the word is found in.
We then store the count of the most frequent word in the page, which we use to calculate tF by dividing each words_to_doc_relevance value of a word
that appears on the page by the max count of that page.
After that, we make a temporary dictionary and loop through every link in the link dictionary to check if the link's title is a title found in the
corpus. If so, we add that link to the temporary dictionary; links to pages that don't exist are ignored. After the loop, we set each value of the 
linking dictionary to the value of the temporary dictionary, thus effectively removing links to non-existent pages.
Now, for every value in the relevance dictionary (the values currently being the tF values), we multiply it by the idf value for the
corresponding word and pages, thus re-populating the relevance dictionary with the final relevance values.
We then go onto weights; we precompute the weight values for the cases of a page linking to nothing (nothing_weight) and when a page links to itself (otherwise_weight).
We then loop through all pages and build up the weight dictionary; if the page has no links, we assume the page links to every page except itself
, so in the cases where the two comparing pages are not the same, we set the weight of the link to the nothing_weight. If a page is something that the other page
links to, then we set the weight to the calculation from the handout (epsilon / total_docs) + ((1 - epsilon) / num_unique_links). If the pages
are the same, we set the weight to the otherwise_weight.
Now for the pagerank, we initialize r and r' and then use a while loop to ensure the distance (calculated by a helper method) is below a certain threshold
delta. In that loop, we set r to r' to store the values and then set r' values to the pagerank calcuation from the handout, storing those values
in the dictionary.

For the query, it takes in the pagerank string and three text files to read from (which were populated with data from the Indexer).
We initialize and populate corresponding dictionaries with data read in from the text files. We use a REPL to take in user input;
when a user inputs ":quit", the program quits. Otherwise, after displaying results, they are prompted to search again.
Before being reprompted, the program scores documents in a function by assigning each page in a dictionary a value based on its relevance and,
if chosen, its pagerank which is added to the relevance. Our program then prints using a helper function the top 10 results from highest to lowest score for
the user to see. If there are less than 10 unique results, the function will print however many unique results are available.

Extra features we included is that we decided to exclude numbers from being detected by our text-specific regex for the sake of getting rid of
extraneous numbers/text that wouldn't relate to most searches.

We tested our program step-by-step for relevances (we don't separately store tF and idf values in separate dictionaries), links, 
pageranks, and distance calculations. Edge cases we considered were every special case for pagerank (pages that link to nothing are 
assume to link to everything except oneself, pages that link to itself have that link ignored and thus are counted as linking to
nothing, pages that link multiple times to another page are counted as only linking once to that page which gets rid of duplicate links,
links to pages not in the corpus are ignored, and meta links are treated like normal links). Weights were likewise tested in a similar 
manner to pagerank as pageranks depend on weights. For relevances, we ensured the relevances were accurate with repeating words, stemmed words,
and stop words.

System tests:

Test searches with multiple words
    Query (no pagerank) - "computer science"
    1. LEO (computer)
    2. Malware
    3. Motherboard
    4. Graphical user interface
    5. PCP
    6. Hacker (term)
    7. Junk science
    8. Gary Kildall
    9. Macro virus
    10. Foonly

    Query (pagerank) - "computer science"
    1. Islamabad Capital Territory
    2. Java (programming language)
    3. Portugal
    4. J?rgen Habermas
    5. Mercury (planet)
    6. Pakistan
    7. Malware
    8. Graphical user interface
    9. LEO (computer)
    10. Isaac Asimov

    Query (no pagerank) - "testing results"
    1. JUnit
    2. GRE Physics Test
    3. Median lethal dose
    4. First-class cricket
    5. Kiritimati
    6. Mendelian inheritance
    7. Autosomal dominant polycystic kidney
    8. Telecommunications in Morocco
    9. Kuomintang
    10. Flying car (aircraft)

    Query (pagerank) - "testing results"
    1. Kuomintang
    2. Netherlands
    3. Northern Hemisphere
    4. Montoneros
    5. Nazi Germany
    6. Pakistan
    7. JUnit
    8. General relativity
    9. GRE Physics Test
    10. Manhattan Project

    Query (no pagerank) - "dog cheese man fight house"
    1. Isle of Man
    2. Cuisine of the Midwestern United States
    3. Limburg
    4. Morphology (linguistics)
    5. LMS
    6. Public house
    7. Fahrenheit 451
    8. Pizza
    9. HOL
    10. Enter the Dragon

    Query (pagerank) - "dog cheese man fight house"
    1. Neolithic
    2. Netherlands
    3. Isle of Man
    4. Morphology (linguistics)
    5. North Pole
    6. Franklin D. Roosevelt
    7. Falklands War
    8. Empress Jit?
    9. Nazi Germany
    10. Normandy

Test searches with multiple duplicate words 
    Query (no pagerank) - "dog dog dog dog"
    1. Morphology (linguistics)
    2. Mustelidae
    3. Kyle MacLachlan
    4. Cuisine of the Midwestern United States
    5. Eth
    6. Phoenix (TV series)
    7. John James Rickard Macleod
    8. James Madison University
    9. Poltergeist
    10. Novial

    Query (pagerank) - "dog dog dog dog"
    1. Morphology (linguistics)
    2. North Pole
    3. Neolithic
    4. Guam
    5. Nazi Germany
    6. Franklin D. Roosevelt
    7. Mustelidae
    8. Pennsylvania
    9. Grammatical gender
    10. Kyle MacLachlan

Test empty searches and searches that are only spaces
    Query (no pagerank) - ""
    No results

    Query (no pagerank) - " "
    No results

Test gibberish
    Query (no pagerank) - "ja;sldkfj;alksdjfa;sdlkf"
    No results

Test search with punctuation
    Query (no pagerank) - "body?!?"
    No results

Test search with numbers (since our indexer does not include numbers in the corpus)
    Query (no pagerank) - "17208372"
    No results

Test search with space before word compared to normal word without spaces
    Query (no pagerank) - " hello"
    1. Java (programming language)
    2. Enjambment
    3. Shoma Morita
    4. Forth (programming language)
    5. Shock site
    6. John Woo
    7. Luxembourgish language
    8. Mandy Patinkin
    9. HAL 9000
    10. Kareem Abdul-Jabbar

    Query (no pagerank) - "hello"
    1. Java (programming language)
    2. Enjambment
    3. Shoma Morita
    4. Forth (programming language)
    5. Shock site
    6. John Woo
    7. Luxembourgish language
    8. Mandy Patinkin
    9. HAL 9000
    10. Kareem Abdul-Jabbar

Test search with all-capital word
    Query (no pagerank) - "HELLO"
    1. Java (programming language)
    2. Enjambment
    3. Shoma Morita
    4. Forth (programming language)
    5. Shock site
    6. John Woo
    7. Luxembourgish language
    8. Mandy Patinkin
    9. HAL 9000
    10. Kareem Abdul-Jabbar