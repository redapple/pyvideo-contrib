# -*- coding: utf-8 -*-
import dateparser

import scrapy

scrapy.selector.SelectorList.get = scrapy.selector.SelectorList.extract_first
scrapy.selector.SelectorList.getall = scrapy.selector.SelectorList.extract

class EuroPython2103Spider(scrapy.Spider):
    name = "europython2013"
    allowed_domains = ["europython.eu"]
    start_urls = (
        'https://ep2013.europython.eu/ep2013/',
    )

    def parse(self, response):
        for talk in response.css('div.page > div.container div.cms > div.talk'):
            yield scrapy.Request(response.urljoin(talk.css('h3 > a::attr(href)').get()),
                                 callback=self.parse_talk)

    def parse_talk(self, response):
        for page in response.css('div.page'):
            yield {
                'source': response.url,
                'title': page.css('h1').xpath('normalize-space()').get(),
                'speakers': page.css('div.page-summary > p > a::text').extract(),
                'description': page.css('div.readonly > div.cms').xpath('string()').get().strip(),
                'description_md': page.css('div.readonly > div.cms').get(),
                'language': page.css('div.talk.details > dl > dt:contains("Language") + dd::text').get(),
                'tags': page.css('div.talk.details span.tag::text').extract(),
                'video': page.css('section.talk.video > iframe::attr(src)').get(),
                'datetime': dateparser.parse(
                    page.css('section.talk.when strong::text').get() + ' 2013'),
            }
