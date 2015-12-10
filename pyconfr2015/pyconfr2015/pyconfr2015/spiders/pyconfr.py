# -*- coding: utf-8 -*-
import re

import dateparser

import scrapy
# I prefer get()
scrapy.selector.SelectorList.get = scrapy.selector.SelectorList.extract_first


class PyConFRTalksSpider(scrapy.Spider):
    name = "pyconfrtalks"
    allowed_domains = ["pycon.fr"]
    start_urls = (
        'http://www.pycon.fr/2015/schedule/',
    )

    def parse(self, response):
        for dateheader in response.css('div.container h3'):
            currdate = dateheader.xpath('string()').get()
            try:
                currdate = dateparser.parse(
                    re.search(ur'^.+\u2014(.+)', currdate, re.I).group(1)
                )
            except:
                currdate = None
            for talk in dateheader.xpath('following-sibling::table[1]').css('td.slot-talk'):
                if not talk.css('span'):
                    continue
                talk_item = {
                    'date': currdate,
                    'title': talk.css('span.title > a::text').get(),
                    'url': response.urljoin(talk.css('span.title > a::attr(href)').get()),
                    'speakers': talk.css('span.speaker').xpath('normalize-space()').get()
                }
                #yield talk_item
                yield scrapy.Request(talk_item['url'],
                                     callback=self.parse_talk_page,
                                     meta={'currdate': currdate})

    def parse_talk_page(self, response):
        self.logger.debug('parse_talk_page')
        for container in response.xpath('.//div[h2 and h4]'):
            yield {
                'title': container.css('h2::text').get(),
                'speakers': container.css('h2 + h4 > a::text').extract(),
                'audience_level': container.xpath('.//dl[dt="Audience level:"]/dd/text()').get(),
                'description': container.css('div.description').xpath('string()').get().strip(),
                'abstract': container.css('div.abstract').xpath('string()').get().strip(),
                'description_md': container.css('div.description').get(),
                'abstract_md': container.css('div.abstract').get(),
                'date': response.meta.get('currdate')
            }
