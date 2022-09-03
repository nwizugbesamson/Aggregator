-- CREATE DATABASE jobs;
\set sch_name `echo $SCHEMA_NAME`
CREATE SCHEMA :sch_name;
CREATE TYPE country_enum AS ENUM(
                    'AUSTRALIA',
                    'USA',
                    'Canada', 
                    'United Kingdom'
                );

CREATE TYPE job_field_enum AS ENUM(
                    'data analyst',
                    'data scientist',
                    'marketing specialist',
                    'product manager', 
                    'software engineer', 
                    'ui ux designer'
                );

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
                'freelance',
                'on call',
                'weekend availability',
                'extended hours',
                'holidays'
            );

CREATE TYPE location_group_enum AS ENUM(
                'remote', 
                'hybrid', 
                'physical location'
            );

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
                    day_of_week DECIMAL(1,0) NULL

                );

\set rd_password `echo $READ_ONLY_PASSWORD`
\set rd_user `echo $READ_ONLY_USER`

COPY indeedjobs FROM '/docker-entrypoint-initdb.d/eda_cleaned.csv' WITH CSV HEADER;
CREATE USER :rd_user WITH PASSWORD :'rd_password';
GRANT CONNECT ON DATABASE jobs TO :rd_user;
GRANT USAGE ON SCHEMA jobs_schema TO :rd_user;
GRANT SELECT ON ALL TABLES IN SCHEMA :sch_name TO :rd_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA :sch_name
GRANT SELECT ON TABLES TO :rd_user;