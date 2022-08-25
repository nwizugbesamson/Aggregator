from datetime import date
import psycopg2 as pg
import pandas as pd
import numpy as np
from creds.creds import READ_ONLY_USER, READ_ONLY_PASSWORD, HOST, PORT, DATABASE_NAME


class DataSchema:
    COMPANY_NAME: str = 'company_name'
    COUNTRY: str = 'country'
    JOB_DESCRIPTION: str = 'job_description'
    JOB_FIELD: str = 'job_field'
    JOB_TITLE: str = 'job_title'
    JOB_TYPE: str = 'job_type'
    NON_REMOTE_LOCATION: str = 'non_remote_location'
    POST_DATE: str= 'post_date'
    RATING: str = 'rating'
    SALARY: str = 'salary'
    CLEAN_LOCATION: str = 'clean_location'
    LOWER_SALARY: str = 'lower_salary_range_usd'
    UPPER_SALARY: str = 'upper_salary_range_usd'
    AVERAGE_SALARY: str = 'average_salary_usd'
    LOCATION_GROUP: str = 'location_group'
    WEEKDAY: str = 'day_of_week'

    



def load_data():
    with pg.connect(user=READ_ONLY_USER, password=READ_ONLY_PASSWORD, host=HOST, port=PORT, database=DATABASE_NAME) as conn:
        data = pd.read_sql('SELECT * FROM public.indeedjobs;', conn, parse_dates=[DataSchema.POST_DATE])
        data = data.replace({'': np.nan, None: np.nan})
    return data