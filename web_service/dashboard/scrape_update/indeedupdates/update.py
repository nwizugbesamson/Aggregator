from requests_html import HTMLSession
from requests import Response
import pandas as pd
from ..resources.utils import  BASE_URLS
from ..resources.cleandata import CleanData
from ..indeedupdates.indeedcron import preprocess_data
import pandas as pd

## class containing data cleaning methods
data_cleaner = CleanData()



def job_data_get(s: HTMLSession, url: str) -> Response:
    """collect div containing job information on provided https://indeed.com url
    
      Args:
            s (_requests_html.HTMLSession_): request session to perform get request
            url (_str_): url to scrape
    """
    # return the elements for each job card
    r = s.get(url)
    return  r.html.find('div.job_seen_beacon')


def _parse_html(url, job, country) -> dict:
    """return dictionary of page data scraped

       Args:
            url (_str_): url of page to be scraped
            job (_str_): job field to collect data on
            country (_str_): country to collect data from
    """

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




def scrape_data() -> pd.DataFrame:
    results = []

    for country, url_list in BASE_URLS.items():
        for url in url_list:
            session = HTMLSession()
            jobs = job_data_get(session, url)
            for job in jobs:
                result = _parse_html(country=country, job=job, url=url)
                results.append(result)

    return preprocess_data(results)

