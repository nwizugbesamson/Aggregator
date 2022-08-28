import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from rake_nltk import Rake
from string import punctuation
import itertools



IRRELEVANT_WORDS= list(stopwords.words('english')) + list(stopwords.words('french')) + list(punctuation)
IRRELEVANT_WORDS.append('…')
IRRELEVANT_WORDS.append('’')
IRRELEVANT_WORDS.append('...')
update_irrelevant_words = ['software', 'development', 'product', 'manager', 'science', 
                           'ui', 'ux', 'products', 'using', 'including', 'engineer', 
                           'engineering', 'teams', 'analysis', 'marketing', 'specialist',
                           'designer', 'designers', 'digital', 'de', 'et', 'closely',
                           'experiences', 'across']
for word in update_irrelevant_words:
    IRRELEVANT_WORDS.append(word)



def extract_keyword_degree(data: pd.DataFrame, nr_of_words:int) -> dict:
    """ extract (nr_of_words) most frequent words from job_description column of dataframe

    Args:
        data (pd.DataFrame): dataframe
        nr_of_words (int): Number of Words to return

    Returns:
        Word_frequency_dictionary (dict): dictionary containing most frequent words and their frequency
    """
    temp_data = data.copy()
    r = Rake()
    r.extract_keywords_from_sentences(temp_data['job_description'].to_list())
    words_freq = r.get_word_degrees()
    sorted_freq = dict(sorted(words_freq.items(), key=lambda item: item[1], reverse=True))
    for word in IRRELEVANT_WORDS:
        if word in sorted_freq:
            del sorted_freq[word]
    return dict(itertools.islice(sorted_freq.items(), 0 ,nr_of_words))