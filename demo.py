from analyzer import Analyzer
from simulation import WordleSimulation
from wordlist import WordList

training_set = WordList(type="training_set").words
dictionary = WordList(type="dictionary").words

optimization_settings_json = {
    "frequency_perc": 0.25,
    "position_perc": 0.75,
    "nonnoun_perc": 0.01,
    "plural_perc": 0.01
}

answer = "GLASS"
starting_word = "ORATE"

wordle_analyzer = Analyzer(words=training_set)
wordle_simulation = WordleSimulation(answer=answer, words=dictionary, wordle_analyzer=wordle_analyzer)

results = wordle_simulation.play_round(json=optimization_settings_json, starting_word=starting_word)
print(results)