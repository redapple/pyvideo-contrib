import collections

import dateparser
from html2text import html2text
import pypandoc
import scrapy


S = scrapy.selector.unified.Selector
SL = scrapy.selector.unified.SelectorList
S.get = S.extract
SL.get = SL.extract_first


class PyConIE2016(scrapy.Spider):
    name = "pyconie2016"
    start_urls = ['https://d6unce.attendify.io/']

    custom_settings = {
        'HTTPCACHE_ENABLED': True
    }
    def parse(self, response):
        talk_ids = collections.defaultdict(list)
        for day in response.css('div.schedule__day.iframe_schedule_day'):
            curr_date = day.css('p.schedule__date::text').get()
            for r in day.css('div::attr(data-link)'):
                talk_ids[r.get()] = curr_date
        yield talk_ids
        for talk in response.css('div.details.uv-card__mask'):
            for session in talk.css('div.uv-card--session'):
                time_of_day = session.css(
                    'span.session__time:nth-child(1)').xpath(
                    'normalize-space()').get()
                talk_id = talk.xpath('@id').get()
                desc = session.css('div.safe-description').get()
                try:
                    desc_md = html2text(desc)
                    desc = pypandoc.convert_text(desc_md, 'rst', format='md')
                except:
                    pass
                yield {'title': session.xpath('string(.//h2)').get(),
                       'datetime': dateparser.parse('{date} {year} {tod}'.format(
                            date=talk_ids[talk_id],
                            year=2016,
                            tod=time_of_day)),
                       'description': desc,
                       'spearkers': session.css('''
                            div.session__speakers-box
                                div.uv-shortcard__title::text''').extract()}
