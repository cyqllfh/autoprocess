import scrapy
from myspider.items import MovieItem,FilmInfoItem

class NuomiSpider(scrapy.Spider):
    name = "nuomi"
    allowed_domains = ["bj.nuomi.com"]
    start_urls = [
        "https://bj.nuomi.com/movie/"
    ]

    def printhxs(self, hxs):
        for i in hxs:
            print i.encode('utf-8')

    def parse(self, response):
        for sel in response.css("div.section-item.clearfix.no-top-border > ul > li > a"):
            movie_item = MovieItem()
            movie_item['name'] = sel.xpath("text()").extract()
            linklist = sel.xpath("@href").extract()
            linklist[0] = "https:" + linklist[0]
            movie_item['link'] = linklist
            if "film" in movie_item['link'][0]:
                yield scrapy.Request(movie_item['link'][0], meta= {'movie_item': movie_item},
                                     callback= self.filminfo_parse)

    def filminfo_parse(self, response):
        movie_item = response.meta['movie_item']

        for sel in response.xpath("//li[@class='cinema']"):
            filminfo_item = FilmInfoItem()
            filminfo_item['name'] = movie_item['name']
            filminfo_item['link'] = movie_item['link']
            filminfo_item['cinema'] = sel.xpath("div/div/div/h3/a/text()").extract()
            filminfo_item['g_price'] = sel.css("div.ci-groupon.clearfix > div ").xpath("span[2]/text()").extract()
            filminfo_item['b_price'] = sel.css("div.ci-book.clearfix > div ").xpath("span[2]/text()").extract()
            yield filminfo_item

        next_page = response.css("div.pager-container")
        subfix = "/0-0/subd/cb0-d10000-s0-o-b1-f0?pn=2"

        if next_page:
            if "=" in response.url:
                url = response.url
                list = url.split("=")
                next_pagenum =  int(list[1]) + 1
                next_url = list[0] + "=" + str(next_pagenum)
            else:
                next_url = movie_item['link'][0] + subfix
            print next_url
            yield scrapy.Request(next_url, meta= {'movie_item': movie_item},
                                 callback=self.filminfo_parse)


