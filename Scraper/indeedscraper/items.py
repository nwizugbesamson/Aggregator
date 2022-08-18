import re
from datetime import datetime, timedelta
import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags

from resources.cleandata import CleanData

# from resources.cleandata import CleanData

data_cleaner = CleanData()

CleanData
    
class IndeedScraperItems(scrapy.Item):
    country = scrapy.Field()
    job_field = scrapy.Field()
    job_title = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    company_name = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    salary = scrapy.Field(input_processor=MapCompose(remove_tags, data_cleaner.clean_salary), output_processor=TakeFirst())
    non_remote_location = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    job_description = scrapy.Field(input_processor=MapCompose(remove_tags, data_cleaner.clean_job_description), output_processor=TakeFirst())
    rating = scrapy.Field(input_processor=MapCompose(remove_tags, data_cleaner.clean_rating), output_processor=Join())
    post_date = scrapy.Field(input_processor=MapCompose(remove_tags, data_cleaner.clean_post_date), output_processor=TakeFirst())
    job_type = scrapy.Field(input_processor=MapCompose(remove_tags, data_cleaner.clean_job_type), output_processor=TakeFirst())






