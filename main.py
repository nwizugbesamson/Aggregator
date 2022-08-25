from Scraper.indeedupdates.update import update_main
from database.dbclass import JobDatabase
from web_service import manage
from creds.creds import READ_ONLY_USER, READ_ONLY_PASSWORD
from eda_aplications.dash_main import dash_main





if __name__ == '__main__':
    # db = JobDatabase()
    # update_main('../data/cron_file.csv')

    # db.create_schema()
    # db.create_indeedjobs_enums()
    # db.create_indeedjobs_table()
    # db.create_read_only_user(READ_ONLY_USER, READ_ONLY_USER)
    # db.insert_indeedjobs('data/eda_cleaned.csv')
    manage.main()
    # dash_main()


