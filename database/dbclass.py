import psycopg2
from ..creds.creds  import PASSWORD, USER, DATABASE_NAME, HOST, READ_ONLY_USER, PORT, SCHEMA_NAME

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

    def connect_pg( func):
        """Decorator function,
           create connection to database for query execution
           pass cursor into function
        """
        def inner_function(*args):
            conn = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE_NAME )
            cursor = conn.cursor()
            func(*(args), _cursor=cursor)
            conn.commit()
            conn.close()
        return inner_function
    

    # database created in command line
    # @connect_pg
    # def create_database(self, _cursor):
    #     create_database = """
    #     CREATE DATABASE %s;
    #     """
    #     _cursor.execute(create_database, (DATABASE_NAME,))

    @connect_pg
    def create_schema(self, _cursor):
        create_schema = """CREATE SCHEMA %s;
        """
        _cursor.execute(create_schema, (SCHEMA_NAME,))
        
        
    

    @connect_pg
    def create_indeedjobs_enums(self, _cursor) -> None:

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

        location_grp_enum = """
            CREATE TYPE location_group_enum AS ENUM(
                'remote', 
                'hybrid', 
                'physical location'
            );
        """
        _cursor.execute(country_enum)
        _cursor.execute(job_field)
        _cursor.execute(job_type)
        _cursor.execute(location_grp_enum)
        
    @connect_pg
    def create_indeedjobs_table(self, _cursor) ->None:

        """create database table for indeed jobs
        """
        table_query = """
                CREATE TABLE IF NOT EXISTS indeedjobs(
                    company_name  VARCHAR(100)  NULL, 
                    country  country_enum    NULL, 
                    job_description  VARCHAR(500)   NULL,
                    job_field  job_field_enum   NULL, 
                    job_title  VARCHAR(300) NULL,
                    job_type  type_enum NULL,
                    non_remote_location   VARCHAR(200)  NULL,
                    post_date   date    NULL, 
                    rating   DECIMAL(2, 1)  NULL, 
                    salary   VARCHAR(15)    NULL,
                    clean_location  VARCHAR(100) NULL,
                    lower_salary_range_usd   DECIMAL(18, 2)  NULL, 
                    upper_salary_range_usd  DECIMAL(18, 2)   NULL,
                    average_salary_usd  DECIMAL(18, 2)   NULL,
                    location_group location_group_enum NULL,
                    day_of_week DECIMAL(1,1) NULL

                );
        
        """

        _cursor.execute(table_query)
        
    @connect_pg
    def insert_indeedjobs(self, filepath, _cursor):
        with open(filepath, "r") as f:
            _cursor.copy_expert("COPY indeedjobs FROM STDIN WITH CSV HEADER", f)


    @connect_pg
    def create_read_only_user(self, _cursor, username, password):
        """Create Read Only User for web service query"""
        create_user = """CREATE USER %s WITH PASSWORD '%s';
                """
        
        allow_connection = """GRANT CONNECT ON DATABASE %s TO %s;
        """

        allow_schema_usage = """GRANT USAGE ON SCHEMA %s TO %s;
        """

        allow_all_tables_select = """GRANT SELECT ON ALL TABLES IN SCHEMA %s TO %s;
        """
        change_default_access = """ALTER DEFAULT PRIVILEGES IN SCHEMA %s
                                   GRANT SELECT ON TABLES TO %s;
        """

        _cursor.execute(create_user, (username, password))
        _cursor.execute(allow_connection, (DATABASE_NAME, username))
        _cursor.execute(allow_schema_usage, (SCHEMA_NAME, username))
        _cursor.execute(allow_all_tables_select, (SCHEMA_NAME, username))
        _cursor.execute(change_default_access, (SCHEMA_NAME, username))







class ReadOnlyDataBase:

    def __init__(self, username, password):
        self.username:str = username
        self.password:str = password


    def connect_pg(self, func):
            def inner_func(*args, **kwargs):
                self: ReadOnlyDataBase = args[0]
                with psycopg2.connect(user=self.username, password=self.password, host=HOST, port=PORT, database=DATABASE_NAME) as conn:
                    cursor = conn.cursor()
                    func(*(args), cursor=cursor, **(kwargs))
                    conn.commit()
            return inner_func

    @connect_pg
    def execute_query(self, query,  cursor, inserts=None):
        """execute and return result of select query on database 

        Args:
            query (str): postgresql query to execute
            cursor (psycopg2.cursor): psycopg2 cursor object
            inserts (tuple || dict, optional): values to insert into query. Defaults to None.
        """
        if inserts is not None:
            cursor.execute(query, inserts)
        else:
            cursor.execute(query)

        return cursor.fetchall()