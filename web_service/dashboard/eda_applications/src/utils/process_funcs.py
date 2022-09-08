import pandas as pd
from nltk.corpus import stopwords
from rake_nltk import Rake
from string import punctuation
import itertools
import numpy as np
from collections.abc import Iterator
from dashboard.eda_applications.src.data.loader import DataSchema


NUMBER_OF_KEYWORDS = 8
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




def return_subset(
                data:list[Iterator[pd.DataFrame]], 
                countries:list[str], 
                job_fields:list[str], 
                cols:list[str]) -> list[pd.DataFrame]:
    """subset iterator of dataframe on countries and job_fields provided

    Args:
        data (list[Iterator[pd.DataFrame]]): iterator of dataset split into groups
        countries (list[str]):list of countries to subset data on
        job_fields (list[str]): list of job_fields to subset data on

    Returns:
        list[pd.DataFrame]: dataframes subset
    """
    if job_fields is None:
        return data[
            (data[DataSchema.COUNTRY].isin(countries))] \
            [cols]\
            .replace({'': np.nan, None: np.nan})
    else:
        return data[
                (data[DataSchema.COUNTRY].isin(countries)) &\
                (data[DataSchema.JOB_FIELD].isin(job_fields)) ]\
                [cols]\
                .replace({'': np.nan, None: np.nan})



def return_subset_single(
                data:list[Iterator[pd.DataFrame]], 
                country:str, 
                job_field:str, 
                cols:list[str]) -> list[pd.DataFrame]:
    """subset iterator of dataframe on countries and job_fields provided

    Args:
        data (list[Iterator[pd.DataFrame]]): iterator of dataset split into groups
        countries (list[str]):list of countries to subset data on
        job_fields (list[str]): list of job_fields to subset data on

    Returns:
        list[pd.DataFrame]: dataframes subset
    """
    if job_field is None:
        return data[
            (data[DataSchema.COUNTRY] == country)] \
            [cols]\
            .replace({'': np.nan, None: np.nan})
    else:
        return data[
                (data[DataSchema.COUNTRY] == country) &\
                (data[DataSchema.JOB_FIELD] == job_field) ]\
                [cols]\
                .replace({'': np.nan, None: np.nan})



def extract_keyword_degree(temp_data: pd.DataFrame, nr_of_words:int) -> dict:
    """ extract (nr_of_words) most frequent words from job_description column of dataframe

    Args:
        data (pd.DataFrame): dataframe
        nr_of_words (int): Number of Words to return

    Returns:
        Word_frequency_dictionary (dict): dictionary containing most frequent words and their frequency
    """
    temp_data
    r = Rake()
    r.extract_keywords_from_sentences(temp_data[DataSchema.JOB_DESCRIPTION].to_list())
    words_freq = r.get_word_degrees()
    sorted_freq = dict(sorted(words_freq.items(), key=lambda item: item[1], reverse=True))
    for word in IRRELEVANT_WORDS:
        if word in sorted_freq:
            del sorted_freq[word]
    return dict(itertools.islice(sorted_freq.items(), 0 ,nr_of_words))



def return_extracted_keywords(data):
    freq_words_general = extract_keyword_degree(data, NUMBER_OF_KEYWORDS)
    if len(freq_words_general) != 0:
        Word, Degree_of_importance = zip(*sorted(freq_words_general.items(), key=lambda item: item[1],))
        return pd.DataFrame({
            'Word': Word,
            'Frequency': Degree_of_importance
        })