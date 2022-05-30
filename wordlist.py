import csv

def load_word_file(file_name):
    words_buffer = []
    with open(file_name, "r") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            words_buffer.append(row[0])
    f.close()
    return(words_buffer)

class WordList:
    def __init__(self, file_name="", type="dictionary"):
        training_set_file = "_input/20220528_previous_results.csv"
        dictionary_file = "_input/dictionary.csv"

        if file_name != "":
            self.words = load_word_file(file_name=file_name)
        elif type == "training_set":
            self.words = load_word_file(file_name=training_set_file)
        else:
            self.words = load_word_file(file_name=dictionary_file)
