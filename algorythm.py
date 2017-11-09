"""
This module transforms txt file into Bag of Words with calculating tf-idf
"""


from sklearn.feature_extraction.text import TfidfVectorizer


def tf_idf(input_text):
    vect = TfidfVectorizer()
    vect.fit_transform(input_text)
    return vect.vocabulary_





