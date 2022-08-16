from requests_html import HTMLSession
import pandas as pd
import numpy as np
from Scraper.resources.utils import  BASE_URLS, COUNTRY_CURRENCY_CONVERSION
from Scraper.resources.cleandata import CleanData

## class containing data cleaning methods
data_cleaner = CleanData()



def job_data_get(s: HTMLSession, url: str) -> list:
    # return the elements for each job card
    r = s.get(url)
    return  r.html.find('div.job_seen_beacon')


def parse_html(url, job, country) -> dict:
    ## parse company name
    try:
        company_name = job.find('span.companyName a')[0].text
    except IndexError:
        company_name = 'Null'

    ## parse job title
    try:
        job_title = job.find('h2.jobTitle span')[0].text
    except IndexError:
        job_title = 'Null'

    ## parse salary
    try:
        salary = job.find('div.salary-snippet-container div')[0].text
        salary = data_cleaner.clean_salary(salary)
    except IndexError:
        salary = 'Null'
    
    ## parse non_remote location
    try:
        non_remote_location = job.find('div.companyLocation')[0].text
    except IndexError:
        non_remote_location = 'Null'

    ## parse job description
    try:
        job_description = job.find('div.job-snippet li')[0].text
        job_description = data_cleaner.clean_job_description()
    except IndexError:
        job_description = 'Null'

    ## parse rating
    try:
        rating = job.find('span.ratingNumber span')[0].text
        rating = data_cleaner.clean_rating(rating)
    except IndexError:
        rating = "Null"

    ## parse post date
    try:
        post_date = job.find('div.result-footer span.date')[0].text
        post_date = data_cleaner.clean_post_date(post_date)
    except IndexError:
        post_date = 'Null'
    
    ## parse job type
    try:
        job_type = job.find('div.tapItem-gutter div.metadata div')[0].text
        job_type = data_cleaner.clean_job_type(job_type)
    except IndexError:
        job_type = 'Null'
    
    job_field = data_cleaner.extract_job_field(url.split('/')[3])

    job_dict = {
                'country': country,
                'job_field': job_field,
                "job_title" : job_title,
                "company_name" : company_name,
                "salary" : salary,
                "non_remote_location" : non_remote_location,
                "job_description" : job_description,
                "rating" : rating,
                "post_date" : post_date,
                'job_type' : job_type,
                }


    return job_dict



def preprocess_data(scraped_data, write_path):
    """format data collected into standard for database

    Args:
        scraped_data (_list_): data collected
        write_path (_str_): path to save formatted file

   
    """


    ## load dataframe
    coltypes = {'salary': str}
    data: pd.DataFrame = pd.DataFrame(scraped_data, dtype=coltypes, na_values=['Null'], parse_dates=['post_date'], index_col=False)


    ##   DROP Unnamed: 0
    data.drop(columns=['Unnamed: 0'], inplace=True)

    ## drop duplicated rows
    data = data.drop_duplicates(subset=['company_name', 'job_description', 'job_title'])


    ## process clean location
    def clean_location(value: str):
        value = value.lower()
        if 'hybrid' in value:
            return 'hybrid'
        if 'remote' in value:
            return 'remote'
        value = value.split(',')[0].split()[0]
        return value


    data['clean_location'] = data['non_remote_location'].apply(clean_location)


    ## process date column
    data['post_date'] = pd.to_datetime(data['post_date'].dt.strftime('%Y-%m-%d'))

    data[['lower_salary_range_usd', 'upper_salary_range_usd']] = data['salary'].str.split('-',expand=True).astype(float, errors='ignore')

    def daily_to_yearly(value:int):
        """return the yearly equivalent pay for jobs with daily pay offers

        Args:
            value (int): integer for operation

        Returns:
            value(int): result of operation
        """
        if len(str(value)) < 4:
            value = value * 260
        return value



    def curr_to_usd(row):
        if row['lower_salary_range_usd'] is not np.nan and row['country'] in COUNTRY_CURRENCY_CONVERSION:
            row['lower_salary_range_usd'] = round(row['lower_salary_range_usd'] * COUNTRY_CURRENCY_CONVERSION[row['country']], 2)
        if row['upper_salary_range_usd'] is not np.nan and row['country'] in COUNTRY_CURRENCY_CONVERSION:
            row['upper_salary_range_usd'] = round(row['upper_salary_range_usd'] * COUNTRY_CURRENCY_CONVERSION[row['country']], 2)
        return row

    data['lower_salary_range_usd'] = data['lower_salary_range_usd'].apply(daily_to_yearly)
    data['upper_salary_range_usd'] = data['upper_salary_range_usd'].apply(daily_to_yearly)

    data = data.apply(curr_to_usd, axis=1)

    data.to_csv(write_path)




def update_main(filepath:str):
    results = []

    for country, url_list in BASE_URLS.items():
        for url in url_list:
            session = HTMLSession()
            jobs = job_data_get(session, url)
            for job in jobs:
                result = parse_html(country=country, job=job, url=url)
                results.append(result)

    preprocess_data(results, filepath)

