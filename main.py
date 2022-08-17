# from Scraper.indeedupdates.update import update_main
# from database.dbclass import JobDatabase
from Tests.test_clean_data import CleanDataTest
from Tests.test_indeedcron import IndeedCronTest
import unittest




if __name__ == '__main__':
    # db = JobDatabase()
    # update_main('../data/cron_file.csv')

    # ## create enum tables
    # db.create_indeedjobs_enums()
    # db.create_indeedjobs_table()


    # db.insert_indeedjobs('data/cleaned_data.csv')
    unittest.main()


