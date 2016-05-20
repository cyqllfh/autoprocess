# -*- coding: UTF-8 -*-

import scrapy
from myspider.items import DoubanMovieItem, DoubanLinkItem

class DoubanMovieSpide(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = [
        # "https://movie.douban.com/subject/25777636/"
        "https://movie.douban.com/top250"
    ]

    def printhxs(self, hxs):
        for i in hxs:
            print i.encode('utf-8')

    def parse(self, response):
        for sel in response.css("div.hd"):
            doubanlink_item = DoubanLinkItem()
            doubanlink_item['title'] = sel.xpath("a/span[1]/text()").extract()
            doubanlink_item['link'] = sel.xpath("a/@href").extract()
            yield scrapy.Request(doubanlink_item['link'][0], self.parse_movie)

        next_page = response.css("span.next a")
        if next_page:
            subfix = response.css("span.next a::attr(href)").extract()
            link = self.start_urls[0] + subfix[0]
            yield scrapy.Request(link, self.parse)

    def parse_movie(self, response):
        item = DoubanMovieItem()
        item['name'] = response.xpath("//div[@id='content']/h1/span/text()").extract()
        for sel in response.xpath("//div[@id='info']"):
            item['director'] = sel.xpath("span[1]/span/a/text()").extract()
            item['scriptwriters'] = sel.xpath("span[2]/span/a/text()").extract()
            item['actors'] = sel.xpath("span[3]/span/a/text()").extract()
            item['genres'] = sel.xpath("//span[@property='v:genre']/text()").extract()
            item['language'] = sel.xpath("text()[count(following-sibling::br) = 5]").extract()
            item['language'] = item['language'][1:]
            item['country'] = sel.xpath("text()[count(following-sibling::br) = 6]").extract()
            item['country'] = item['country'][1:]
        item['rating_num'] = response.css("div.rating_self.clearfix  strong::text").extract()
        item['descriptions'] = response.css("span.all.hidden::text").extract()

        yield item