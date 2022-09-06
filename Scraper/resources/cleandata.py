import re
import numpy as np
from datetime import datetime, timedelta
from Scraper.resources.utils import PATTERNS, UNDEFINED_LIST


class CleanData:
    """provide data cleaning methods for scraped data"""


    def extract_job_field(self, url: str) -> str:
        """extracts job field from request """


        for field in PATTERNS:
            for pattern in PATTERNS[field]:
                if pattern in url.lower():
                    return field
        


    def clean_rating(self, value: str) -> float:
        """pre_process rating data"""
        return float(value.strip())


    def clean_salary(self, value: str) -> str:
        """pre process salary data"""
        return re.sub(r'[^K.–\d-]', '', value).replace('–', '-')


    def clean_post_date(self, value: str) -> str:
        """return job posted date as float"""
        value = value.replace('Posted', '').replace('+', '').replace('Employer', '').replace('Active', '').strip().split()[0]
        n_days_ago = 0 if value in['Just', 'Today', 'Now', 'Hiring', 'today']  else int(value)
        today = datetime.today()
        target_date = today - timedelta(days=n_days_ago)        
        return target_date.strftime('%Y-%m-%d')

    def clean_job_description(self, value: str):
        return value.replace('\n', '')


    def clean_job_type(self, value):
        """format raw data from job type column to usable data

        Args:
            value (str): raw_data

        Returns:
            str: formatted data
        """
        
        for label in UNDEFINED_LIST:
            if label in value:
                value =  'undefined'
        value = re.sub('[\d+]', '', value).lower()
        result = 'contract' if 'fixed term' in value or 'contract' in value or 'casual' in value else value
        result = 'internship' if 'temp to perm'in result else result
        result =  result.replace('/ co-op', '').strip()
        return result


    