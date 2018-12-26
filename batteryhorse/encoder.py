"""
BatteryHorse: Encode/Decode binary data as English sentences
https://github.com/cstranex/batteryhorse
(C) Copyright 2018 Chris Stranex <chris@stranex.com>
"""
import os
import sys
import argparse
from functools import lru_cache
import nltk
from nltk.corpus import wordnet
from .version import __version__

try:
    from secrets import choice
except ImportError:
    from random import SystemRandom
    choice = SystemRandom().choice


def _filter_words(word):
    return word.isalpha() and len(word) > 1


@lru_cache()
def _get_words():
    nltk_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
    if nltk_path not in nltk.data.path:
        nltk.data.path.insert(0, nltk_path)

    verbs = sorted({word.lower() for word in filter(
        _filter_words, wordnet.all_lemma_names(wordnet.VERB))})
    verb_size = len(verbs)

    nouns = sorted({word.lower() for word in filter(
        _filter_words, wordnet.all_lemma_names(wordnet.NOUN))})
    noun_size = len(nouns)

    adjs = sorted({word.lower() for word in filter(
        _filter_words, wordnet.all_lemma_names(wordnet.ADJ))})
    adj_size = len(adjs)

    conjs = sorted(['and', 'or', 'lest', 'till', 'nor',
                    'but', 'yet', 'so', 'unless', 'when'])
    conj_size = len(conjs)

    return (verbs, verb_size, nouns, noun_size, adjs, adj_size, conjs, conj_size)


def encode_data(data: bytes) -> str:
    """Creates a sentence encoding the hashed data given above. The output is one or more
    sentences with the format Verb Noun Adjective Conjunction Adjective."""

    VERBS, VERB_SIZE, NOUNS, NOUN_SIZE, ADJS, ADJ_SIZE, CONJS, CONJ_SIZE = _get_words()

    sentences = []
    sentence = []
    value = int.from_bytes(data, byteorder='big', signed=False)
    while value > 0:
        if len(sentence) == 0:  # Verb
            value, offset = divmod(value, VERB_SIZE)
            sentence.append(VERBS[offset].capitalize())
        elif len(sentence) == 1:  # Noun
            value, offset = divmod(value, NOUN_SIZE)
            sentence.append(NOUNS[offset])
        elif len(sentence) == 3:  # Conjunction
            value, offset = divmod(value, CONJ_SIZE)
            sentence.append(CONJS[offset])
        elif len(sentence) in (2, 4):  # Adjective
            value, offset = divmod(value, ADJ_SIZE)
            sentence.append(ADJS[offset])
        elif len(sentence) == 5:  # Sentence break
            sentences.append(' '.join(sentence))
            sentence = []
    sentences.append(' '.join(sentence))
    return '. '.join(sentences).strip()


def decode_data(string: str, length: int) -> bytes:
    """Extract the hash of the encoded data from the given string of sentences created
    with encode_data."""
    VERBS, VERB_SIZE, NOUNS, NOUN_SIZE, ADJS, ADJ_SIZE, CONJS, CONJ_SIZE = _get_words()
    parts = [
        (ADJS, ADJ_SIZE),
        (CONJS, CONJ_SIZE),
        (ADJS, ADJ_SIZE),
        (NOUNS, NOUN_SIZE),
        (VERBS, VERB_SIZE)
    ]
    sentences = string.lower().split('.')
    sentences.reverse()
    value = 0
    for sentence in sentences:
        words = sentence.split()
        words.reverse()
        # Start at an offset if necessary if we do not have a full sentence (ie: partial block)
        max_parts = len(parts) - len(words)
        for n, word in enumerate(words, start=max_parts):
            word = word.strip()
            dictionary, size = parts[n]
            index = dictionary.index(word)
            value = index + (value * size)
    return value.to_bytes(length=length, byteorder='big', signed=False)


def create_secret(size=3):
    """Creates a random sentence that can be used as a passphrase"""
    VERBS, VERB_SIZE, NOUNS, NOUN_SIZE, ADJS, ADJ_SIZE, CONJS, CONJ_SIZE = _get_words()
    words = []
    for _ in range(size):
        words.append(choice(NOUNS + VERBS))
    return ' '.join(words).capitalize()


def main():
    """Run Batteryhorse in the terminal"""
    parser = argparse.ArgumentParser(
        prog="batteryhorse", description="Encode and decode data as sentences")
    parser.add_argument('--encode', action='store_true',
                        help='Accept data to be encoded from STDIN')
    parser.add_argument('--decode', action='store_true',
                        help='Accept data to be decoded from STDIN')
    parser.add_argument('--generate', action='store_true',
                        help='Generate a random secret')
    parser.add_argument(
        '--length',
        help='Specify the length of secret or data to be decoded',
        default=20,
        type=int
    )
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__)

    args = parser.parse_args()

    if args.encode:
        data = sys.stdin.read()
        print(encode_data(data.encode('ascii')))
    elif args.decode:
        data = sys.stdin.read()
        print(decode_data(data, args.length).decode('ascii'))
    elif args.generate:
        print(create_secret(args.length))
    else:
        print(parser.print_usage())


if __name__ == '__main__':
    main()
