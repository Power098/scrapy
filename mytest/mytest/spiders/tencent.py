# -*- coding: utf-8 -*-
import scrapy
from  mytest.items import MytestItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    offset = 0
    baseURL = 'https://hr.tencent.com/position.php?lid=&tid=&keywords=%E8%AF%B7%E8%BE%93%E5%85%A5%E5%85%B3%E9%94%AE%E8%AF%8D&start='
    start_urls = [baseURL + str(offset)]

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for node in node_list:
            item = MytestItem()
            item['positionName'] = node.xpath("./td[1]/a/text()").extract()[0]
            item['positionLink'] = node.xpath("./td[1]/a/@href").extract()[0]
            if len(node.xpath("./td[2]/text()").extract()) >0:
                item['positionType'] = node.xpath("./td[2]/text()").extract()[0]
            else:
                item['positionType'] = ''
            item['peopleNumber'] = node.xpath("./td[3]/text()").extract()[0]
            item['workLocation'] = node.xpath("./td[4]/text()").extract()[0]
            item['publishTime'] = node.xpath("./td[5]/text()").extract()[0]

            yield item

        if self.offset < 2820:
            self.offset += 10
            url = self.baseURL + str(self.offset)
            yield scrapy.Request(url, callback=self.parse)

