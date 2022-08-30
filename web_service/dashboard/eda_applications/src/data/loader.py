import os
import psycopg2 as pg
import pandas as pd
import numpy as np



READ_ONLY_USER = os.environ.get('POSTGRES_USER')
READ_ONLY_PASSWORD = os.environ.get('READ_ONLY_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
DATABASE_NAME = os.environ.get('DATABASE_NAME')


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
    print('ABOUT TO CONNECT TO DATBASE!!!!!!!!!!!!')
    with pg.connect(user=READ_ONLY_USER, password=READ_ONLY_PASSWORD, host=POSTGRES_HOST, port=POSTGRES_PORT, database=DATABASE_NAME) as conn:
        print('DATBASE CONNECTION SUCCESSFUL!!!!!!!!!!!!')
        data = pd.read_sql('SELECT * FROM indeedjobs;', conn, parse_dates=[DataSchema.POST_DATE])
        data = data.replace({'': np.nan, None: np.nan})
    return data