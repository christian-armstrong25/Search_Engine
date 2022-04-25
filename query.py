class Query:
    def __init__(self) -> None:
        while (True):
            input = input("Search: ")
            if input == ":quit":
                break
            else:
                print(input.upper())
