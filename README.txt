# Wiki Search Engine

## Group Members
- Christian Armstrong
- Daniel Liu

## Introduction
This project implements a simple search engine for Wikipedia-like XML dumps. It indexes pages, computes relevance and importance scores, and allows users to search for pages using a command-line interface.

## Usage

### 1. Indexing
Run the indexer to process an XML wiki dump and generate index files:

```
python index.py <XML filepath> <titles filepath> <docs filepath> <words filepath>
```
- `<XML filepath>`: Path to the XML file to index.
- `<titles filepath>`: Output file for ID-Title pairs.
- `<docs filepath>`: Output file for ID-PageRank pairs.
- `<words filepath>`: Output file for Word-ID-Relevance triples.

### 2. Querying
Run the querier to search the indexed data:

```
python query.py [--pagerank] <titleIndex> <documentIndex> <wordIndex>
```
- `--pagerank` (optional): If present, search results consider PageRank in ranking.
- `<titleIndex>`: File with ID-Title pairs (from indexer).
- `<documentIndex>`: File with ID-PageRank pairs (from indexer).
- `<wordIndex>`: File with Word-ID-Relevance triples (from indexer).

You will be prompted to enter search queries. Type `:quit` to exit.

## Algorithms

### TF-IDF (Term Frequency-Inverse Document Frequency)
- **Purpose:** Measures how important a word is to a document in the corpus.
- **How:**
  - For each word in a page, compute term frequency (TF) as the count of the word divided by the max word count in that page.
  - Compute inverse document frequency (IDF) as `log(total_docs / docs_with_word)`.
  - The relevance score for a word in a page is `TF * IDF`.
  - Stop words and numbers are excluded; words are stemmed.

### PageRank
- **Purpose:** Measures the importance of a page based on the link structure.
- **How:**
  - Build a directed graph where nodes are pages and edges are links between them.
  - Use the PageRank algorithm (with damping factor epsilon) to iteratively update scores until convergence.
  - Special cases:
    - Pages linking to nothing are treated as linking to all other pages (except themselves).
    - Self-links and duplicate links are ignored.
    - Links to non-existent pages are ignored.

### Query Scoring
- For each query, compute a relevance score for each page based on the sum of TF-IDF scores for the query words.
- If `--pagerank` is specified, add the PageRank score to the relevance score.
- Return the top 10 results (or fewer if less available).

## Features
- Excludes numbers and stop words from indexing.
- Handles edge cases in link graph (self-links, dead links, duplicates).
- Stems words for better matching.
- Interactive REPL for searching.

## Testing & Edge Cases
- Handles empty queries, queries with only spaces, gibberish, punctuation, and numbers.
- Tested with multiple and duplicate words, case insensitivity, and leading/trailing spaces.

## Example Test Results

**Query (no pagerank):** `computer science`
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

**Query (pagerank):** `computer science`
1. Islamabad Capital Territory
2. Java (programming language)
3. Portugal
4. Jürgen Habermas
5. Mercury (planet)
6. Pakistan
7. Malware
8. Graphical user interface
9. LEO (computer)
10. Isaac Asimov

**Query (no pagerank):** `testing results`
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

**Query (pagerank):** `testing results`
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

**Query (no pagerank):** `dog cheese man fight house`
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

**Query (pagerank):** `dog cheese man fight house`
1. Neolithic
2. Netherlands
3. Isle of Man
4. Morphology (linguistics)
5. North Pole
6. Franklin D. Roosevelt
7. Falklands War
8. Empress Jitō
9. Nazi Germany
10. Normandy

**Query (no pagerank):** `dog dog dog dog`
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

**Query (pagerank):** `dog dog dog dog`
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

**Query (no pagerank):** `""` (empty)
- No results

**Query (no pagerank):** ` " "` (spaces)
- No results

**Query (no pagerank):** `ja;sldkfj;alksdjfa;sdlkf` (gibberish)
- No results

**Query (no pagerank):** `body?!?` (punctuation)
- No results

**Query (no pagerank):** `17208372` (numbers)
- No results

**Query (no pagerank):** ` hello` (leading space)
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

**Query (no pagerank):** `hello`
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

**Query (no pagerank):** `HELLO` (all caps)
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

---

## Known Bugs
None