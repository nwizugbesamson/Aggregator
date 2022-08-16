import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from indeedscraper.items import IndeedScraperItems
from scrapy.loader import ItemLoader
import time
from resources.utils import  START_URLS, ALLOWED_DOMAINS
from resources.cleandata import CleanData






def extract_country(url: str) -> str:
    """extract country information from request"""
    return 'Canada' if 'ca' in url else ('United Kingdom'if 'uk' in url else ('AUSTRALIA' if 'au' in url else 'USA'))


data_cleaner = CleanData()





class IndeedSpider(scrapy.Spider):
    """Web crawler class for indeed scraper

    Subclass of scrapy.spider

    Yields:
        _ItemLoader_: _scraped data from crawler_
    """
    name = 'indeed'
    allowed_domains = ALLOWED_DOMAINS
    start_urls = START_URLS
    handle_httpstatus_list = [403, 307, 301]
    

    def parse(self, response: scrapy.Selector):
        """recursively parse data from http response recieved

        Args:
            response (scrapy.Selector): _selector object from http response_

        Yields:
            _ItemLoader_: _dataclass of parsed data_
        """
        for job in response.css('div.job_seen_beacon'):
            loader = ItemLoader(item=IndeedScraperItems(), selector=job)
            url: str = response.request.url
            url = url.split('/')

            country = extract_country(url[2])
            job_field = data_cleaner.extract_job_field(url[3])

            loader.add_value('country', country)
            loader.add_value('job_field', job_field)
            loader.add_css("job_title", 'h2.jobTitle span')
            loader.add_css("company_name", 'span.companyName')
            loader.add_css("salary", 'div.salary-snippet-container div')
            loader.add_css("non_remote_location", 'div.companyLocation')
            loader.add_css("job_description", 'div.job-snippet')
            loader.add_css("rating", 'span.ratingNumber span')
            loader.add_css("post_date", 'div.result-footer span.date')
            loader.add_css('job_type', 'div.tapItem-gutter div.metadata div')

            yield loader.load_item()

        ## throttle request rate to avoid bot detection
        ## redundant with autothrottle setting
        # TODO 1. TEST AUTHTHROTTLE, DOWNLOAD DELAY SETTINGS
        time.sleep(3)

        ## follow next page and recursively call self.parse()
        next_page = response.css('ul.pagination-list a[aria-label=Next]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
                

    

process = CrawlerProcess(get_project_settings())