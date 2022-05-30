# Wordle Monte Carlo framework/toolkit
This started from an argument (as all good projects do!) over Wordle starter words and guesses.

There seemed to be preferences in Josh Wardle's previous word picks (in particular - he seems to avoid plurals and non-nouns).  Why not do a 30 minute analysis, right?

The 30 minute analysis to get to those answers (indeed it's incredibly probable for the answer to be a singular noun, historically - *tough luck, Mike*) turned into a question of "will a Monte Carlo simulation reveal optimal play strategy?"  So, here we are.

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
from wordlist import WordList

training_set = WordList(type="training_set").words
dictionary = WordList(type="dictionary").words

optimization_settings_json = {
    "frequency_perc": 0.75,
    "position_perc": 0.25,
    "nonnoun_perc": 0.25,
    "plural_perc": 0.25
}

answer = "GLASS"
starting_word = "ORATE"

wordle_analyzer = Analyzer(words=training_set)
wordle_simulation = WordleSimulation(answer=answer, words=dictionary, wordle_analyzer=wordle_analyzer)

results = wordle_simulation.play_round(json=optimization_settings_json, starting_word=starting_word)
```

An example implementation is provided in example.py. 

## Scoring:
Scoring is **very** basic at this point.  Analyzer.score_word(s) will return a score based on the provided optimization settings JSON.  In short - the current scoring algorithm applies a multiplier against letter frequency, letter position, being a noun vs. not, being plural.

This can certainly be more sophisticated by expanding the settings JSON and updating score_word to reflect.

## Game Results
Game.compare_guess_vs_answer will return a JSON object containing the results from a guess against a known answer.  The first element contains "yellow"/partial matches, while the following 5 elements contain specifics about each position.  Example (our guess "ORATE" vs. "CLEAN"):
```
[
    {
        "yellow": [
            "a",
            "e"
        ]
    },
    {
        "black": [
            "o",
            "r",
            "t"
        ],
        "green": ""
    },
    {
        "black": [
            "o",
            "r",
            "t"
        ],
        "green": ""
    },
    {
        "black": [
            "o",
            "r",
            "a",
            "t"
        ],
        "green": ""
    },
    {
        "black": [
            "o",
            "r",
            "t"
        ],
        "green": ""
    },
    {
        "black": [
            "o",
            "r",
            "t",
            "e"
        ],
        "green": ""
    }
]
```

## Notes:
- Albeit sometimes clunky, we avoid loading/scoring the full dictionary wherever possible.  In testing, this has been far and away the biggest performance drain.
