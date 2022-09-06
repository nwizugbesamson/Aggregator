import os
import psycopg2 as pg
import pandas as pd
import numpy as np
from psycopg2.extensions import AsIs





READ_ONLY_USER = os.environ.get('POSTGRES_USER')
READ_ONLY_PASSWORD = os.environ.get('READ_ONLY_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')


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


data_columns = (
                AsIs(DataSchema.COUNTRY),
                AsIs(DataSchema.JOB_FIELD), 
                AsIs(DataSchema.AVERAGE_SALARY), 
                AsIs(DataSchema.CLEAN_LOCATION), 
                AsIs(DataSchema.COMPANY_NAME), 
                AsIs(DataSchema.JOB_TYPE),
                AsIs(DataSchema.RATING),
                AsIs(DataSchema.JOB_DESCRIPTION),
                AsIs(DataSchema.LOCATION_GROUP),
                )
    
def load_data():
    with pg.connect(user=READ_ONLY_USER, password=READ_ONLY_PASSWORD, host=HOST, port=PORT, database=DATABASE_NAME) as conn:
        data = pd.read_sql_query('SELECT country, job_field, average_salary_usd, company_name, job_description,  job_type, clean_location,  location_group, rating FROM public.indeedjobs;',
                            conn, 
                            chunksize=4500,
                            dtype={
                                DataSchema.COUNTRY : 'category',
                                DataSchema.JOB_FIELD : 'category',
                                DataSchema.JOB_TYPE : 'category',
                                DataSchema.LOCATION_GROUP : 'category',
                            }
                            )
    return data