# Wordle Monte Carlo framework/toolkit
This started from an argument (as all good projects do!) over Wordle starter words and guesses.

There seemed to be preferences in Josh Wardle's previous word picks (in particular - he seems to avoid plurals and non-nouns).  Why not do a 30 minute analysis, right?

The 30 minute analysis to get to those answers (indeed it's incredibly probable for the answer to be a singular noun, historically - tough luck, Mike) turned into a question of "will a Monte Carlo simulation reveal optimal play strategy?"  So, here we are.

The modules in this repo should serve as a reasonably decent basis to get started on Wordle Monte Carlo simulation and optimization.

## Classes:
- Analyzer: Scoring logic that creates probabilities, ranks, or "top 1" given a list of words and set of rules.
- Predictor/PredictorCollection: Contains valid "guesses", updates based on guess results provided.
- Game: Basic implementation of the Wordle game logic/engine - provides guess results (in JSON format, per below) given an answer, guess.
- WordleSimulation: Harness that combines the moving pieces to play/attempt to optimize a game.

## Usage example:
```
from analyzer import Analyzer
from simulation import WordleSimulation

# Realistically, these should be loaded from larger lists - see "/_input/"
training_set = ["glass", "scour", "being", "delve", "yield"]
dictionary = ["first", "water", "after", "where", "right"]

answer = "GLASS"
starting_word = "ORATE"

wordle_analyzer = Analyzer(words=training_set)
wordle_simulation = WordleSimulation(answer=answer, words=dictionary, wordle_analyzer=wordle_analyzer)

results = wordle_simulation.play_round(json={{optimization_settings_json}}, starting_word=starting_word)
```

An example implementation is provided in example.py. 

## Notes:
- Albeit sometimes clunky, I avoid loading/scoring the full dictionary wherever possible.  In testing, this has been far and away the biggest performance drain.
- 
