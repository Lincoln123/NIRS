from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer

def tf_idf(input_text):

    '''
    includes Bag od words and tf-idf transformation
    :param input_text:
    :return:
    '''

    vect = TfidfVectorizer()
    X_train = vect.fit_transform(input_text)


    return X_train


'''
Testing code


bards_words =["The fool doth think he is wise,",
"but the wise man knows himself to be a fool"]


def bag_of_words(input_text):

    vect = CountVectorizer().fit(input_text)
    X_train = vect.transform(input_text).toarray()
    print(X_train)
    print(TfidfTransformer().fit_transform(X_train))
    print('___________________________________________________-')
    #print(vect.vocabulary_)
    #print(vect.get_feature_names())
    return X_train
'''




