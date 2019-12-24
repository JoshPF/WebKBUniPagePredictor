import sys
import os
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import words
import nltk.classify.util

stop_words = set(stopwords.words('english'))

def calculate_freq_dist(feature, pred_univ, num_common_words):
    word_count = 0
    # all the keywords for the directory
    all_keywords = []

    # loop through the directory given as a command line argument
    for uni_directory in os.listdir(feature):
        uni_directory_loc = os.path.join(feature, uni_directory)
        # Don't include the university used for testing set
        if uni_directory_loc.lower() == pred_univ.lower():
            continue
        # loop through each univeristy directory
        for filename in os.listdir(uni_directory_loc):
            # create the path for the current file in the directory
            location = os.path.join(uni_directory_loc, filename)
            # print (location)

            all_keywords.extend(find_keywords(location))

    # calculate the frequency of the words and display the 50 most common
    freq_dist = nltk.FreqDist(all_keywords)
    freq_dist = freq_dist.most_common(int(num_common_words))
    keyword_weights = calculate_weights(freq_dist)
        
    keywords = []
    for tup in keyword_weights:
        keywords.append(tup[0])

    return keywords, keyword_weights
    #return all_keywords

def find_keywords(location):
    all_keywords = list()
    # open the current file
    with open(location, 'rb') as f:
        # ignore MIME header
        trimmed = b' '.join(line.strip() for line in f.readlines()[5:])
        # parse through the text with beautiful soup and get only the text
        soup = BeautifulSoup(trimmed, 'html.parser')
        file_text = soup.get_text()

        tokenizer = RegexpTokenizer(r'\w+')
        file_text_tokenized = tokenizer.tokenize(file_text)

        # remove stopwords
        #keywords_file_text = [word for word in file_text_tokenized if word.lower() not in stop_words]
        keywords_file_text = []
        for word in file_text_tokenized:
            if word.lower() not in stop_words and len(word) > 1:
                try:
                    int(word)
                    continue
                except ValueError:
                    keywords_file_text.append(word.lower())

        all_keywords += keywords_file_text
        return all_keywords

def calculate_weights(keyword_tuples):
    tot = 0
    for tup in keyword_tuples:
        tot += tup[1]
    keyword_weights = []
    for tup in keyword_tuples:
        weight = tup[1]/tot
        keyword_weights.append( (tup[0], weight) )
    return keyword_weights