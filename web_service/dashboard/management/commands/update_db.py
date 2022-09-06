"""
Django command to wait for the database to be available.
"""
from dashboard.scrape_update.indeedupdates.update import scrape_data

from psycopg2 import OperationalError as Psycopg2OpError
import psycopg2 as pg
import os

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

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
            data = scrape_data()
            with pg.connect(user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST, port=POSTGRES_PORT, database=POSTGRES_DB) as conn:
                data.to_sql('public.indeedjobs', conn, if_exits='append')

        except (Psycopg2OpError, OperationalError):
            print('Update Failed!!!!!')     
