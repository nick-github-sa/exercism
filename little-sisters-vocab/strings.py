"""Functions for creating, transforming, and adding prefixes to strings."""

def add_prefix_un(word):
    return 'un' + word

def make_word_groups(vocab_words):
    prefix = vocab_words[0]
    return ' :: '.join([prefix] + [prefix + w for w in vocab_words[1:]])

def remove_suffix_ness(word):
    stem = word[:-4]  # remove "ness"
    if stem.endswith("i"):
        stem = stem[:-1] + "y"
    return stem

def adjective_to_verb(sentence, index):
    words = sentence.split()
    word = words[index].strip(".,!?")
    return word + "en"
