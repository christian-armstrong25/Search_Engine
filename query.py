from file_io import read_docs_file, read_title_file, read_words_file
import sys
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))


class Querier():
    def __init__(self, titles, docs, words) -> None:
        self.ids_to_titles = {}
        read_title_file(titles, self.ids_to_titles)
        self.ids_to_pageranks = {}
        read_docs_file(docs, self.ids_to_pageranks)
        self.words_to_doc_relevance = {}
        read_words_file(words, self.words_to_doc_relevance)

    def score_docs(self, search) -> None:
        for word in search:
            word = PorterStemmer().stem(word)
            if word not in STOP_WORDS and word in self.words_to_doc_relevance:
                for id in self.words_to_doc_relevance[word]:
                    self.ids_to_relevance[id] += self.words_to_doc_relevance[word][id]
        if sys.argv[1] == "--pagerank":
            for docs in self.ids_to_relevance:
                self.ids_to_relevance[docs] *= self.ids_to_pageranks[docs]

    # 6. takes in two lists and returns a sorted list made up of the content within the two lists

    def merge(self, left, right):
        # 7. Initialize an empty list output that will be populated with sorted elements.
        # Initialize two variables i and j which are used pointers when iterating through the lists.
        output = []
        i = j = 0

        # 8. Executes the while loop if both pointers i and j are less than the length of the left and right lists
        while i < len(left) and j < len(right):
            # 9. Compare the elements at every position of both lists during each iteration
            if left[i][1] < right[j][1]:
                # output is populated with the lesser value
                output.append(left[i])
                # 10. Move pointer to the right
                i += 1
            else:
                output.append(right[j])
                j += 1
        # 11. The remnant elements are picked from the current pointer value to the end of the respective list
        output.extend(left[i:])
        output.extend(right[j:])

        return output

    def merge_sort(self, list):
        # 2. List with length less than is already sorted
        if len(list) == 1:
            return list

        # 3. Identify the list midpoint and partition the list into a left_partition and a right_partition
        mid_point = len(list) // 2

        # 4. To ensure all partitions are broken down into their individual components,
        # the merge_sort function is called and a partitioned portion of the list is passed as a parameter
        left_partition = self.merge_sort(list[:mid_point])
        right_partition = self.merge_sort(list[mid_point:])

        # 5. The merge_sort function returns a list composed of a sorted left and right partition.
        return self.merge(left_partition, right_partition)

    def print_top_10(self):
        sorted_list = self.merge_sort(list(self.ids_to_relevance.items()))
        for i in range(min(10, len(sorted_list))):
            print(str(i + 1) + ". " + self.ids_to_titles[sorted_list[i][0]])
        print("")


if __name__ == "__main__":
    command_index = 0
    if sys.argv[1] == "--pagerank":
        command_index = 1
    query = Querier(sys.argv[1 + command_index], sys.argv[2 + command_index],
                    sys.argv[3 + command_index])
    print("\n")
    while (True):
        query.ids_to_relevance = dict.fromkeys(query.ids_to_titles.keys(), 0)
        user_input = input("Search: ")
        if user_input == ":quit":
            break
        else:
            query.score_docs(user_input.split())
            query.print_top_10()
