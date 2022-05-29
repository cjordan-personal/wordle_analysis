def has_eliminated_letter(letter, eliminated_letters):
    if letter in eliminated_letters:
        return (True)
    else:
        return (False)

def has_confirmed_letter(letter, confirmed_letter):
    if letter == confirmed_letter or confirmed_letter == "":
        return (True)
    else:
        return (False)

def has_partial_letter_matches(word, partial_letters, guess_results):
    for i in range(0, len(partial_letters)):
        is_partial_match = False
        for j in range(0, len(word)):
            if guess_results[j + 1]["green"] != partial_letters[i] and partial_letters[i] == word[j]:
                is_partial_match = True
        if not is_partial_match:
            return (False)
    return (True)

class Predictor:
    def __init__(self, word):
        self.word = word.lower()
        pass

    def is_valid_word_vs_guess_result(self, guess_result):
        is_possible = True
        for i in range(0, len(self.word)):
            if has_eliminated_letter(self.word[i], guess_result[i + 1]["black"]):
                is_possible = False
                break
            if not has_confirmed_letter(self.word[i], guess_result[i + 1]["green"]):
                is_possible = False
                break

        if not has_partial_letter_matches(self.word, guess_result[0]["yellow"], guess_result):
            is_possible = False

        return (is_possible)

class PredictorCollection:
    def __init__(self, words):
        self.predictor_list = words
        self.predictors = []
        for word in words:
            predictor = Predictor(word=word)
            self.predictors.append(predictor)

    def slice_to_valid_guesses(self, guess_result):
        predictors = []
        for predictor in self.predictors:
            if predictor.is_valid_word_vs_guess_result(guess_result=guess_result):
                predictors.append(predictor)
        self.predictors = predictors

    def words(self):
        word_list = []
        for predictor in self.predictors:
            word_list.append(predictor.word)
        return(word_list)