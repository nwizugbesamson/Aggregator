import psycopg2
from ..creds.creds  import PASSWORD, USER

class JobDatabase:
    """Setup class for database initialization
    """
    """
        connection decorator function
        create table
        insert files
        delete duplicates
        return queries
    """

    def connect_pg( user, password, host, port, database):
        """Decorator function,
           create connection to database for query execution
           pass cursor into function
        """
        def wrapper(func):
            def inner_function(*args):
                conn = psycopg2.connect(user=user, password=password, host=host, port=port, database=database )
                cursor = conn.cursor()
                func(*(args), cursor=cursor)
                conn.commit()
                conn.close()
            return inner_function
        return wrapper

    @connect_pg(user=USER, password=PASSWORD, host='localhost', port='5432', database='JOBS')
    def create_indeedjobs_enums(self, cursor) -> None:

        """create enum types for indeedjobs"""
        country_enum = """
                CREATE TYPE country_enum AS ENUM(
                    'AUSTRALIA',
                    'USA',
                    'Canada', 
                    'United Kingdom'
                );

        """

        job_field = """
                CREATE TYPE job_field_enum AS ENUM(
                    'data analyst',
                    'data scientist',
                    'marketing specialist',
                    'product manager', 
                    'software engineer', 
                    'ui ux designer'
                );

        """

        job_type = """
            CREATE TYPE type_enum AS ENUM(
                'undefined', 
                'graduate', 
                'full-time', 
                'permanent', 
                'contract',
                'part-time', 
                'internship', 
                'apprenticeship', 
                'temporary',
                'freelance'
            );
        """
        cursor.execute(country_enum)
        cursor.execute(job_field)
        cursor.execute(job_type)
        
    @connect_pg(user=USER, password=PASSWORD, host='localhost', port='5432', database='JOBS')
    def create_indeedjobs_table(self, cursor) ->None:

        """create database table for indeed jobs
        """
        table_query = """
                CREATE TABLE IF NOT EXISTS indeedjobs(
                    company_name  VARCHAR(100)  NULL, 
                    country  VARCHAR(15)    NULL, 
                    job_description  VARCHAR(500)   NULL,
                    job_field  job_field_enum   NULL, 
                    job_title  VARCHAR(300) NULL,
                    job_type  type_enum NULL,
                    non_remote_location   VARCHAR(200)  NULL,
                    post_date   date    NULL, 
                    rating   DECIMAL(2, 1)  NULL, 
                    salary   VARCHAR(15)    NULL,
                    clean_location  VARCHAR(50) NULL,
                    lower_salary_range   DECIMAL(9, 2)  NULL, 
                    upper_salary_range  DECIMAL(9, 2)   NULL
                );
        
        """

        cursor.execute(table_query)
        
    @connect_pg(user=USER, password=PASSWORD, host='localhost', port='5432', database='JOBS')
    def insert_indeedjobs(self, filepath, cursor):
        with open(filepath, "r") as f:
            cursor.copy_expert("COPY indeedjobs FROM STDIN WITH CSV HEADER", f)