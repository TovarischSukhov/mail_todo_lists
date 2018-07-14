# coding: utf-8
import json
import time

import pandas as pd
from lazy import lazy
from nltk import word_tokenize


class Speller:
    def __init__(self, counter_filename, letters_typos_counter_filename, typical_typos_filename, bigrams_filename,
                 fix_register=False, verbose=False, try_split=True, use_language_model=True, custom_words_file=None):
        self._counter_filename = counter_filename
        self.custom_words_file = custom_words_file
        self._letters_typos_counter_json_filename = letters_typos_counter_filename
        self._fn_typical_json_filename = typical_typos_filename
        self._bigrams_filename = bigrams_filename

        self.fix_register = fix_register
        self.try_split = try_split
        self.use_language_model = use_language_model
        self.verbose = verbose
        self.get_words = word_tokenize
        self._letters = u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя-"

        # settings for tuning on test set; now set by only common sense
        self._p_lambda_freq = 0.9
        self._p_lambda_typo = 1.35
        self._filter_probs_lm = 0.001
        self._multiplier_to_min_lm_prob = 0.01

        # based on raw dataset from https://github.com/dkulagin/kartaslov/tree/master/dataset/orfo_and_typos
        # plans to recount it based on assesors manual job and wiki changing history
        self._p_miss = 0.05670836177413011
        self._p_extra = 0.0594795414324915
        self._p_letter_2_letter = 0.07536170981381378

    @lazy
    def words_counter(self):
        # taking csv/csv.zip file like
        """
        lowered     num         type    top_form
        в           19363596    NaN     NaN
        ..
        iphone      6308        other   iPhone
        ..
        """
        try:
            df = pd.read_csv(self._counter_filename, compression='gzip')
        except:
            df = pd.read_csv(self._counter_filename)
        if self.custom_words_file:
            df = pd.concat([df, pd.read_csv(self.custom_words_file)])
        words_number = df.num.sum()
        milion = [
            'милион', 'милиона', 'милионы', 'милионов',
            'милиону', 'милионам', 'милионом', 'милионами',
            'милионе', 'милионах',
        ]
        df = df.drop(df.loc[df['word'].isin(milion)].index)
        words_counter = dict()
        for row in df.as_matrix():
            words_counter[row[0]] = (row[1] / words_number, row[2], row[3])
        return words_counter

    @lazy
    def letter_typos_stat(self):
        with open(self._letters_typos_counter_json_filename) as f:
            letters_stat = json.loads(f.read())
        return letters_stat

    @lazy
    def typical_typos_dict(self):
        with open(self._fn_typical_json_filename) as f:
            typical_typos_dict = json.loads(f.read())
        return typical_typos_dict

    @lazy
    def bigram_stat(self):
        # bigrams = {"политическая": {"компания": 0.0001, "кампания": 0.02}}
        df = pd.read_csv(self._bigrams_filename)
        bigrams = dict()
        total_word_entries = df.num.sum()
        for w1, w2, n in zip(df.word1, df.word2, df.num):
            bigrams[w1] = bigrams.get(w1, dict())
            bigrams[w1][w2] = n / total_word_entries
        self._lm_missed_word_p = df.num.iloc[-1] / total_word_entries * self._multiplier_to_min_lm_prob
        return bigrams

    def _P_aprior(self, word_to):
        word_info = self.words_counter.get(word_to)
        p = word_info[0] if word_info else 0
        return p

    def _P_typo(self, word_from, word_to):
        p = 1
        if word_from != word_to:
            words_len_diff = len(word_from) - len(word_to)
            if words_len_diff == 0:
                for l1, l2 in zip(word_from, word_to):
                    if l1 != l2:
                        p *= self._p_letter_2_letter
                        letter_stat = self.letter_typos_stat.get(l1)
                        if letter_stat:
                            p *= letter_stat.get(l2) or 1
            else:
                p_per_letter = self._p_miss if words_len_diff > 0 else self._p_extra
                p *= p_per_letter ** abs(words_len_diff)

                # todo: process prob of transpositions
                # todo: process prob of doubling letters
        return p

    def _P_word(self, word_from, word_to):
        p_aprior = self._P_aprior(word_to)
        p_aprior_adj = p_aprior ** self._p_lambda_freq
        p_typo = self._P_typo(word_from, word_to)
        p_typo_adj = p_typo ** self._p_lambda_typo
        p_result = p_aprior_adj * p_typo_adj
        if self.verbose:
            template = "{:20} -> {:20}: p_aprior_adj = {:.7f}, p_typo_adj = {:.7f}, p_word = {:.11f}"
            print(template.format(word_from, word_to, p_aprior_adj, p_typo_adj, p_result))
        return p_result

    def _filter_only_known(self, words):
        return set(w for w in words if w in self.words_counter)

    def _edits1(self, word):
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in self._letters]
        inserts = [L + c + R for L, R in splits for c in self._letters]
        return set(deletes + transposes + replaces + inserts)

    def _candidates(self, word):
        return self._filter_only_known(self._edits1(word))

    def _move_register(self, word_from, word_to):
        if word_from[0] == word_from[0].upper():
            word_to = word_to.capitalize()
        else:
            word_to = word_to.lower()
        return word_to

    def _word_fix_register(self, word_lowered_fixed, query):
        response = None
        word_info = self.words_counter.get(word_lowered_fixed)
        if word_info:
            word_type = word_info[1]
            if word_type == 'up':
                response = word_lowered_fixed.upper()
            elif word_type == 'cap':
                response = word_lowered_fixed.capitalize()
            elif word_type == 'other':
                response = word_info[2]
        response = response or self._move_register(word_from=query, word_to=word_lowered_fixed)
        return response

    def _fix_register(self, word_lowered_fixed, query):
        words = word_lowered_fixed.split()
        response = " ".join([self._word_fix_register(w, query if i == 0 else "l") for i, w in enumerate(words)])
        return response

    def _word_is_known(self, word_lowered):
        t = word_lowered if word_lowered in self.words_counter else None
        if self.verbose and t:
            print('word {} is known'.format(t))
        return t

    def _fix_word(self, word_lowered, prev_word_lowered=None):
        response = None
        candidates = self._candidates(word=word_lowered)
        if candidates:
            if len(candidates) == 1:
                response = list(candidates)[0]
                if self.verbose:
                    print('got 1 candidate for "{}":'.format(word_lowered), response)
            else:
                probs = [self._P_word(word_lowered, cand) for cand in candidates]
                probs_and_cands = [(prob, cand) for prob, cand in zip(probs, candidates)]
                probs_and_cands = sorted(probs_and_cands, reverse=True)
                response = probs_and_cands[0][1]
                probs_and_cands_with_lm = []

                if self.use_language_model and prev_word_lowered:
                    max_prob = probs_and_cands[0][0]
                    filtered_probs_and_cands = [(prob, cand) for prob, cand in probs_and_cands if
                                                prob > max_prob * self._filter_probs_lm]
                    if len(filtered_probs_and_cands) > 1:
                        second_word_probabilities = self.bigram_stat.get(prev_word_lowered)
                        if second_word_probabilities:
                            probs_and_cands_with_lm = [
                                (prob * second_word_probabilities.get(cand, self._lm_missed_word_p), cand) for
                                prob, cand in probs_and_cands]
                            probs_and_cands_with_lm = sorted(probs_and_cands_with_lm, reverse=True)
                            response = probs_and_cands_with_lm[0][1]
                if self.verbose:
                    max_prob = max(probs)
                    print('got several candidates for "{}":'.format(word_lowered),
                          [(p / max_prob, c) for p, c in (probs_and_cands_with_lm or probs_and_cands)])
        return response

    def _word_correction(self, word, fix_register=None, prev_word_lowered=None):
        word_lowered = word.lower()
        if len(word) >= 2:
            resp = None
            typical_fix = self.typical_typos_dict.get(word_lowered)
            if typical_fix:
                resp = typical_fix
            elif word_lowered.isalpha():
                resp = self._word_is_known(word_lowered) or self._fix_word(word_lowered, prev_word_lowered)
            resp = resp or word_lowered
        else:
            resp = word_lowered
        if fix_register:
            resp = self._fix_register(resp, word)
        return resp

    def __call__(self, text, fix_register=None):
        fix_register = fix_register if fix_register is not None else self.fix_register
        words = self.get_words(text)
        fixed_words = []
        for w in words:
            fixed_words.append(self._word_correction(w, fix_register, fixed_words[-1] if fixed_words else None))
        text = " ".join(fixed_words).replace(' , ', ', ').replace(' . ', '. ')
        return text


if __name__ == '__main__':
    fn_dict = 'data/word_freq_dict.csv.zip'
    fn_letters = 'data/letter_typos_matrix.json'
    fn_typical = 'data/typical_typos.json'
    fn_bigrams = 'data/bigrams.zip'
    speller = Speller(
        fn_dict,
        fn_letters,
        fn_typical,
        fn_bigrams,
        fix_register=True,
        verbose=True,
        try_split=True,
        custom_words_file='data/custom_realty_words.csv',
    )
    while True:
        t = input('word: ')
        tic = time.time()
        resp = speller(t)
        print("time spent: {:.2f}ms".format(1000 * (time.time() - tic)))
        print("response:", resp)
        print('\n------\n')
