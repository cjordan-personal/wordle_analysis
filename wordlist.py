import csv
from wordfreq import zipf_frequency

def load_word_file(file_name):
    words_buffer = []
    with open(file_name, "r") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            words_buffer.append(row[0])
    f.close()
    return(words_buffer)

def slice_by_popularity(words, limit):
    if limit == 0:
        limit = len(words)
    popularity = {}

    for word in words:
        popularity[word.lower()] = zipf_frequency(word.lower(), lang="en")

    return(list(dict(sorted(popularity.items(), key=lambda item: item[1], reverse=True)).keys())[:limit])

class WordList:
    def __init__(self, file_name="", type="dictionary", limit=0):
        training_set_file = "_input/20220528_previous_results.csv"
        dictionary_file = "_input/dictionary.csv"

        if file_name != "":
            self.words = load_word_file(file_name=file_name)
        elif type == "training_set":
            self.words = load_word_file(file_name=training_set_file)
        else:
            self.words = load_word_file(file_name=dictionary_file)

        if limit > 0:
            self.words = slice_by_popularity(words=self.words, limit=limit)