from analyzer import top_result

class WordleSimulation:
    def __init__(self, answer, wordle_game, wordle_analyzer, wordle_predictors):
        self.answer = answer
        self.analysis_dictionary = []
        self.wordle_analyzer = wordle_analyzer
        self.wordle_game = wordle_game
        self.wordle_predictors = wordle_predictors

    def guess(self, json, starting_word, current_guess=""):
        if current_guess == "":
            return(starting_word)
        else:
            guess_result = self.wordle_game.compare_guess_vs_answer(guess=current_guess)
            self.wordle_predictors.slice_to_valid_guesses(guess_result=guess_result)

        scoring = self.wordle_analyzer.score_words(words=self.wordle_predictors.words(), json=json)
        current_guess = top_result(scoring)
        return(current_guess)