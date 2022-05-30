from analyzer import Analyzer, top_result
import json
import os
from postgres_engine import Table
import random
from simulation import WordleSimulation
from wordlist import WordList

words_training_set = WordList(type="training_set").words
words_dictionary = WordList(type="dictionary").words

table = Table(name="wordle", primary_key="_id", connection_url=os.environ["POSTGRES_URL_MONTECARLO"])

wordle_analyzer = Analyzer(words=words_training_set)

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
    for answer in words_training_set:
        wordle_simulation = WordleSimulation(answer=answer, words=words_dictionary, wordle_analyzer=wordle_analyzer)
        current_guess = ""

        results = wordle_simulation.play_round(json=json_values, starting_word=starting_word)
        print("\t** Results for '" + answer.lower() + "'...")
        print(results)
        print("")
        table.upsert(object=results)