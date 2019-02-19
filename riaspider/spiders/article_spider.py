import scrapy
from scrapy_splash import SplashRequest


class RiaSpider(scrapy.Spider):
    name = 'article_spider'
    start_urls = ["https://ria.ru/20190218/1550997539.html"]  # TODO

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5, 'images_enabled': False})

    def parse(self, response):
        title = response.xpath('//meta[@property="og:title"]/@content').get()
        text = '\n'.join(response.css('.article__text ::text').getall())
        keywords = response.xpath('//meta[@name="keywords"]/@content').get()

        yield {
            'title': title,
            'text': text,
            'keywords': keywords,
            'url': response.request.url,
            'author': response.css('.article__author-name ::text').get()
        }

        for next_page in response.css('a.recommend__item-title'):
            yield response.follow(next_page, self.parse)
