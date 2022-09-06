from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError
import psycopg2 as pg
import os


UPDATE_QUERY = """
DELETE FROM public.indeedjobs
WHERE ctid in (
            SELECT ctid FROM(
                        SELECT 
                            *, 
                            row_number() over (partition by company_name, country, job_description, job_field, job_title) as rn
                        FROM public.indeedjobs
                            ) dup_flag
                        WHERE dup_flag > 1
                        );
"""

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')




class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        try:
            with pg.connect(user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST, port=POSTGRES_PORT, database=POSTGRES_DB) as conn:
                cursor = conn.cursor()
                cursor.execute(UPDATE_QUERY)
                conn.commit()

        except (Psycopg2OpError, OperationalError):
            print('DUPLICATE DATA DELETION FAILED!!!!!')     
