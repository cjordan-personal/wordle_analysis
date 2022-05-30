from analyzer import Analyzer, top_result
from datetime import datetime
from game import Game
import hashlib
from predictor import PredictorCollection

class WordleSimulation:
    def __init__(self, answer, words):
        self.answer = answer.lower()
        self.wordle_game = Game(answer=answer)
        self.wordle_predictors = PredictorCollection(words=words)
        self.analysis_dictionary = []
        self.wordle_analyzer = Analyzer(words=words)

    def guess(self, json, current_guess=""):
        guess_result = self.wordle_game.compare_guess_vs_answer(guess=current_guess)
        self.wordle_predictors.slice_to_valid_guesses(guess_result=guess_result)
        scoring = self.wordle_analyzer.score_words(words=self.wordle_predictors.words(), json=json)
        current_guess = top_result(scoring)

        return(current_guess)

    def play_round(self, json, starting_word):
        json_results = []

        # Need to add flexibility for where starting word is not provided.
        for i in range(0, 6):
            json_result = json.copy()

            if i == 0:
                current_guess = starting_word
            else:
                current_guess = self.guess(json=json, current_guess=current_guess)

            json_result["answer"] = self.answer.lower()
            json_result["guess"] = current_guess
            json_result["guess_count"] = i + 1
            json_result["_id"] = hashlib.md5(str(json_result).encode(encoding="utf-8")).hexdigest()
            json_result["_at"] = str(datetime.utcnow())

            json_results.append(json_result)
            if current_guess == self.answer or i == 5:
                return(json_results)