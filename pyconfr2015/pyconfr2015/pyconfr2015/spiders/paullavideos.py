# -*- coding: utf-8 -*-
import scrapy
from w3lib.url import safe_download_url


class PauLLAVideosSpider(scrapy.Spider):
    name = 'paullavideos'
    allowed_domains = ['paulla.asso.fr']
    start_urls = (
        'http://video-pyconfr2015.paulla.asso.fr/',
    )

    def parse(self, response):
        for link in response.css('ul > li > a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(link),
                                 callback=self.parse_video_page)

    def parse_video_page(self, r):
        yield {
            'page_url': r.url,
            'title': r.css('article > h1::text').get(),
            'videos': [
                {'src': safe_download_url(r.urljoin(src.xpath('@src').get())),
                 'type': src.xpath('@type').get()}
                for src in r.css('video > source')
            ],
            'video_thumbnail': safe_download_url(
                r.urljoin(r.css('video::attr(poster)').get())),
        }
