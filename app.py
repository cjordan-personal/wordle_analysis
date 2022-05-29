from analyzer import Analyzer
import csv
from datetime import datetime
from game import Game
import hashlib
import json
import os
from postgres_engine import Table
from predictor import PredictorCollection
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

# Randomization
frequency_perc = random.choice([0.25, 0.5, 0.75, 0.8, 0.9, 1])
json_values = {
    "frequency_perc": frequency_perc,
    "position_perc": 1-frequency_perc,
    "nonnoun_perc": random.choice([0.25, 0.5, 0.75, 0.8, 0.9, 1]),
    "plural_perc": random.choice([0.25, 0.5, 0.75, 0.8, 0.9, 1])
}

table = Table(name="wordle", primary_key="_id", connection_url=os.environ["POSTGRES_URL_MONTECARLO"])

c = 0

while 0 == 0:
    answer = random.choice(words_historical).lower()
    print(answer)
    wordle_game = Game(answer=answer)
    wordle_analyzer = Analyzer(words=words_historical)
    wordle_predictors = PredictorCollection(words=words_dictionary)
    wordle_simulation = WordleSimulation(answer=answer, wordle_game=wordle_game, wordle_analyzer=wordle_analyzer, wordle_predictors=wordle_predictors)
    current_guess = ""

    json_values["answer"] = answer
    for i in range(0, 6):
        current_guess = wordle_simulation.guess(json=json_values, current_guess=current_guess)

        json_values["_at"] = str(datetime.utcnow())
        json_values["guess"] = current_guess
        json_values["_id"] = hashlib.md5((json_values["_at"] +
                                          json_values["guess"] +
                                          json_values["answer"]).encode(encoding="utf-8")).hexdigest()
        json_values["guess_count"] = i + 1
        print(json.dumps(json_values))
        table.upsert(object=[json_values])
        if current_guess == wordle_game.answer:
            break

    c = c + 1
    #if c > 5:
    #   break