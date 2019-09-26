import scrapy
import re
from pathlib import Path

class HltvSpider(scrapy.Spider):
    # spider config
    name = "hltv"
    base_url = 'https://www.hltv.org'

    save_dir = Path('data')

    start_urls = [f'{base_url}/events/archive?eventType=MAJOR&offset=0']            

    def parse(self, response):
        """
        Gets all the events from the start_urls event pages
        """

        # if there are more pages, in the category, we also scrap them
        page_count = response.xpath("//span[@class='pagination-data']/text()").get()
        match = re.match(r'\d+ - (\d+) of (\d+)', page_count).groups() # e.g. 1 - 50 of 324
        assert len(match) == 2, "Hltv's page structure might have changed"
        current, total = match
        if int(current) < int(total): # we load next page if more are available
            url = re.sub(r'offset=\d+', f'offset={current}', response.url)            
            yield scrapy.Request(url=url, callback=self.parse)

        # scrap all available matches
        for href in response.xpath("//div[@class='events-page']/div[@class='events-month']/a/@href").getall():
            event_number = href.split('/')[2]
            yield scrapy.Request(
                url=f'{self.base_url}/results?event={event_number}', 
                callback=self.parse_event,
            )

    def parse_event(self, response):
        """
        Gets all the matches of a given event
        """

        for href in response.xpath("//div[@class='result-con']/a/@href").getall():
            yield scrapy.Request(
                url=f'{self.base_url}{href}',
                callback=self.parse_match,
            )

    def parse_match(self, response):
        """
        Saves the metadata of a match for convinience later
        We are mostly intereseted in the demos url
        """
        demo_href = response.xpath("//div[@class='stream-box']/a[contains(text(), 'GOTV Demo')]/@href").get()
        dir_name = response.url.split('/')[-1]

        maps = response.xpath("//div[@class=' played']/div/div[@class='mapname']/text()").getall() # only played ones
        if len(maps) <= 0: # some older events didn't use the 'played' class, unplayed was not displayed
            maps = response.xpath("//div[@class='mapname']/text()").getall()

        teams = response.xpath("//div[@class='teamName']/text()").getall()

        yield {
            'match_url': response.url,
            'demo_url': f"{self.base_url}{demo_href}",
            'dir_name': dir_name,
            'maps': maps,
            'teams': teams,
        }
