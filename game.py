def is_letter_green(guess_letter, word_letter):
    if guess_letter == word_letter:
        return (True)
    else:
        return (False)

class Game:
    def __init__(self, answer):
        self.answer = answer.lower()

    def compare_guess_vs_answer(self, guess):
        # Initialize guess results object.
        guess = guess.lower()
        guess_result = [{"black": [], "green": ""} for i in range(0, 6)]
        guess_result[0] = {"yellow": []}

        # Parse exact matches
        for i in range(0, len(guess)):
            if is_letter_green(guess[i], self.answer[i]):
                guess_result[i + 1]["green"] = guess[i]

        yellow_list = []
        for i in range(0, len(guess)):
            is_black = True
            for j in range(0, len(self.answer)):
                if guess[i] == self.answer[j]:
                    # Omit where we have an exact match already.
                    if guess_result[i + 1]["green"] == guess[i] or guess_result[j + 1]["green"] == self.answer[j]:
                        # Don't quite understand why I need this, has to do with handling of multiples with an exact match.
                        if i != j:
                            is_black = False
                    # Where the match isn't exact.
                    else:
                        yellow_list.append(guess[i])
                        guess_result[i + 1]["black"].append(guess[i])
                        is_black = False
                        # If a matching yellow is found, exit loop (can only flag once per guess).
                        break

            if is_black:
                for k in range(0, len(guess)):
                    if self.answer[k] != guess[k]:
                        guess_result[k + 1]["black"].append(guess[i])

        guess_result[0]["yellow"] = yellow_list
        return (guess_result)