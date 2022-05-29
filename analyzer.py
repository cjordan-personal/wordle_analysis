import inflect
from nltk.corpus import wordnet
import string

def score_word_by_result_table(word, result_table):
    alpha_count_tracker = dict.fromkeys(string.ascii_lowercase, 0)
    score = 0
    for i in range(0, len(word)):
        score = score + result_table[alpha_count_tracker[word[i].lower()]][word[i].lower()]
        alpha_count_tracker[word[i].lower()] = alpha_count_tracker[word[i].lower()] + 1
    return (score)

def rank_result_set(words_result_set, method="high"):
    if method == "low":
        return ({key: rank for rank, key in enumerate(sorted(words_result_set, key=words_result_set.get), 1)})
    else:
        return (
        {key: rank for rank, key in enumerate(sorted(words_result_set, key=words_result_set.get, reverse=True), 1)})

def top_result(words_result_set, method="high"):
    return(next(iter(rank_result_set(words_result_set=words_result_set, method=method))))

def tally_to_prob(tally_table):
    total_letters = 0
    for result in tally_table:
        total_letters = total_letters + sum(result.values())

    for i in range(0, 5):
        for k in tally_table[i].keys():
            tally_table[i][k] = tally_table[i][k] / total_letters

    return (tally_table)

def is_noun(word):
    syns = wordnet.synsets(word)
    if syns[0].lexname().split('.')[0] if syns else None == "noun":
        return(True)
    else:
        return(False)

def is_plural(word):
    inf = inflect.engine()
    return(inf.singular_noun(word))

class Analyzer:
    def __init__(self, words):
        self.words = words

    def score_word(self, word, json):
        frequency_perc = json["frequency_perc"] if "frequency_perc" in json.keys() else 1
        position_perc = json["position_perc"] if "position_perc" in json.keys() else 0
        nonnoun_perc = json["nonnoun_perc"] if "nonnoun_perc" in json.keys() else 1
        plural_perc = json["plural_perc"] if "plural_perc" in json.keys() else 1

        nonnoun_mult = nonnoun_perc if not is_noun(word) else 1
        plural_mult = plural_perc if is_plural(word) else 1

        results = (score_word_by_result_table(word=word,
                                              result_table=tally_to_prob(self.letter_tally_by_frequency())) * frequency_perc + score_word_by_result_table(word=word,
                           result_table=tally_to_prob(self.letter_tally_by_position())) * position_perc) * nonnoun_mult * plural_mult
        return(results)

    def score_words(self, words, json):
        results = {}
        for word in words:
            results[word] = self.score_word(word=word, json=json)
        return(results)

    def letter_tally_by_position(self):
        letters = []
        for i in range(0, 5):
            alpha = dict.fromkeys(string.ascii_lowercase, 0)
            for word in self.words:
                alpha[word[i].lower()] = alpha[word[i].lower()] + 1
            letters.append(alpha)
        return (letters)

    def letter_tally_by_frequency(self):
        letter_tally = []

        for i in range(0, 5):
            letter_tally.append(dict.fromkeys(string.ascii_lowercase, 0))

        for word in self.words:
            alpha_count_tracker = dict.fromkeys(string.ascii_lowercase, 0)
            for i in range(0, len(word)):
                letter_tally[alpha_count_tracker[word[i].lower()]][word[i].lower()] = \
                    letter_tally[alpha_count_tracker[word[i].lower()]][word[i].lower()] + 1
                alpha_count_tracker[word[i].lower()] = alpha_count_tracker[word[i].lower()] + 1

        return (letter_tally)