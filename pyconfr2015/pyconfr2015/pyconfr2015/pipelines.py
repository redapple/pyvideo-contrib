# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import html2text

class Html2TextPipeline(object):
    def process_item(self, item, spider):
        for f in ('description_md', 'abstract_md'):
            val = item.get(f)
            if val:
                item[f] = html2text.html2text(val)
        return item
