from analyzer import Analyzer, top_result
import csv
import json
import os
from postgres_engine import Table
import random
from simulation import WordleSimulation

def load_word_file(file_name):
    words_buffer = []
    with open(file_name, "r") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            words_buffer.append(row[0])
    f.close()
    return(words_buffer)

historical_file = "_input/20220528_previous_results.csv"
words_historical = load_word_file(file_name=historical_file)
dictionary_file = "_input/dictionary.csv"
words_dictionary = load_word_file(file_name=dictionary_file)

table = Table(name="wordle", primary_key="_id", connection_url=os.environ["POSTGRES_URL_MONTECARLO"])

wordle_analyzer = Analyzer(words=words_historical)

while 0 == 0:
    json_values_used = []
    # Loop until we find a permutation that hasn't been used yet.
    # Not the most efficient, but will be most flexible as more parameters are added.
    while 0 == 0:
        frequency_perc = random.choice([0, 0.25, 0.5, 0.75, 1])
        json_values = {
            "frequency_perc": frequency_perc,
            "position_perc": 1 - frequency_perc,
            "nonnoun_perc": random.choice([0.01, 0.1, 0.5, 1]),
            "plural_perc": random.choice([0.01, 0.1, 0.5, 1])
        }
        if json_values not in json_values_used:
            json_values_used.append(json_values)
            break

    starting_word = top_result(wordle_analyzer.score_words(words=words_dictionary, json=json_values))
    print("* Starting analysis using starting word '" + starting_word + "' and randomization values:")
    print(json.dumps(json_values, indent=4))

    # Traverse entire historical answer list using one randomization profile.
    for answer in words_historical:
        wordle_simulation = WordleSimulation(answer=answer, words=words_dictionary, wordle_analyzer=wordle_analyzer)
        current_guess = ""

        results = wordle_simulation.play_round(json=json_values, starting_word=starting_word)
        print("\t** Results for '" + answer.lower() + "'...")
        print(results)
        print("")
        table.upsert(object=results)