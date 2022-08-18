# Write your code here
from nltk.tokenize import regexp_tokenize
from collections import defaultdict, Counter
from random import choices, choice
import re

class TextProb:
    def __init__(self, file: str):
        with open(file, encoding="utf-8") as f:
            self.corpus = regexp_tokenize(f.read(), r"\S+")

        self.token_count = len(self.corpus)
        self.unique_tokens = len(set(self.corpus))
        self.bigrams = {n: [self.corpus[n], self.corpus[n + 1]] for n in range(len(self.corpus))
                        if n < len(self.corpus) - 1}

        self.trigrams = {f'{self.corpus[n]} {self.corpus[n + 1]}': self.corpus[n + 2] for n in range(len(self.corpus))
                        if n < len(self.corpus) - 2}
        self.markov = defaultdict(list)
        self.markov_trigram = defaultdict(list)

        for i in self.bigrams.values():
            head = i[0].strip()
            tails = i[1]
            self.markov[head].append(tails)
        for n, j in self.markov.items():
            self.markov[n] = Counter(self.markov[n]).most_common()

        for i, j in self.trigrams.items():
            k = i.split()
            head = f'{k[0]} {k[1]}'
            tails = j
            self.markov_trigram[head].append(tails)

        self.bigrams_count = len(self.bigrams)

    def get_index(self, n: str) -> str:
        try:
            return self.corpus[int(n)]
        except IndexError:
            return 'Index Error. Please input an integer that is in the range of the corpus.'
        except (TypeError, ValueError):
            return 'Type Error. Please input an integer.'

    def get_bigram_index(self, n: str) -> str:
        try:
            if int(n) < 0:
                return f'Head: {self.bigrams[len(self.corpus) - abs(int(n)) - 1][0]}\t\t' \
                       f'Tail: {self.bigrams[len(self.corpus) - abs(int(n)) - 1][1]}'
            else:
                return f'Head: {self.bigrams[int(n)][0]}\t\tTail: {self.bigrams[int(n)][1]}'

        except (IndexError, KeyError):
            return 'Index Error. Please input an integer that is in the range of the corpus.'
        except (TypeError, ValueError):
            return 'Type Error. Please input an integer.'

    def get_markov_chains(self, key: str) -> bool:
        x = self.markov.get(key)
        if x is None:
            print(f'Key Error. The requested word is not in the model. Please input another word.')
            return False
        print(f"Head: {key}")
        for i, j in x.items():
            print(f'Tail: {i}  Count: {j}')

    def get_random_text(self):
        starting_word = choice(self.corpus)
        prev_word = starting_word
        sentences = []

        for _ in range(10):
            sentence = []
            for _ in range(10):
                next_words, weights = list(zip(*self.markov[prev_word]))
                next_word = choices(next_words, weights=weights)[0]
                sentence.append(next_word)
                prev_word = next_word
            sentences.append(' '.join(sentence))

        return '\n'.join(sentences)

    def get_correct_sentence(self):
        texts = [" ".join(i.split()) for i in self.markov_trigram.keys() if re.fullmatch(r"[A-Z]{1}[a-z]+", i.split()[0])]
        sentences = []
        for _ in range(10):
            first_head = choice(texts)
            prev_word = first_head
            sentence = [first_head]
            last_word = prev_word.split()[1]
            while True:
                next_word = self.markov_trigram[prev_word]
                to_concatenate = next_word[0]
                prev_word = f'{last_word} {to_concatenate}'
                last_word = prev_word.split()[1]
                sentence.append(last_word)
                if len(sentence) > 3:
                    if bool(re.match(r"^[A-z]+[.!?]+$", last_word)):
                        sentences.append(' '.join(sentence))
                        break

        return '\n'.join(sentences)

    def __str__(self):
        all_tokens = f'All tokens: {self.token_count}'
        unique_tokens = f'Unique tokens: {self.unique_tokens}'
        return f'Corpus statistics\n{all_tokens}\n{unique_tokens}\n'


x = TextProb(input())
print(x.get_correct_sentence())

