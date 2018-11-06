import collections
import re

import dateparser
from html2text import html2text
import pypandoc
import scrapy



class PyConIT2018(scrapy.Spider):
    name = "pyconit2018"
    start_urls = [
        'https://www.pycon.it/p3/schedule/pycon9/'
    ]

    custom_settings = {
        'HTTPCACHE_ENABLED': True,
        #'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        for day in response.css('div.schedule'):
            ds = day.xpath('normalize-space(.//h2)').get()
            dt = dateparser.parse(ds)
            self.logger.debug(dt)

            for talk in day.css('div.track div.event'):
                speakers = talk.css('.speakers > a').xpath('normalize-space()').extract()
                data = {
                    'title': talk.css('.name').xpath('normalize-space()').get(),
                    'speakers': speakers,
                    'short_speakers': speakers,
                    'datetime': dt
                    }
                self.logger.debug(data)
                link = talk.css('.name > a::attr(href)').get()
                if link:
                    #continue
                    yield scrapy.Request(response.urljoin(link),
                                         callback=self.parse_talk,
                                         meta={'talk': data})
                    #break
                else:
                    yield data

    def parse_talk(self, response):
        data = response.meta['talk']
        data['speakers'] = response.css('div.talk-speakers > a').xpath('normalize-space()').extract()
        description = response.css('div.readonly').get()
        if description:
            desc_md = html2text(description)
            desc_rst = pypandoc.convert_text(desc_md, 'rst', format='md')
            data['description'] = desc_rst

        for details in response.css('div.details'):
            language = details.xpath('.//dt[.="Language" or .="Lingua"]/following-sibling::dd[1]/text()').get('').lower()
            data['language'] = language
            data['tags'] = details.css('div.all-tags span::text').getall()
            data['related_urls'] = [response.urljoin(u)
                                    for u in details.xpath('.//a[starts-with(., "Download")]/@href').getall()]
            break

        yield data
