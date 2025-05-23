import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stem(word):
    stemmed_tokens = stemmer.stem(word.lower())
    filtered_tokens = [token for token in stemmed_tokens if token not in stop_words]  
    return filtered_tokens


def bag_of_words(tokenized_sentence, words):
    sentence_words = [stem(word) for word in tokenized_sentence]
  
    bag = np.zeros(len(words), dtype=np.float32)
    for index, word in enumerate(words):
        if word in sentence_words: 
            bag[index] = 1

    return bag