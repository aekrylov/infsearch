import scrapy


class RiaSpider(scrapy.Spider):
    name = 'ria_spider'
    start_urls = ["https://ria.ru/20190218/1550997539.html"]  # TODO

    def parse(self, response):
        title = response.xpath('//meta[@property="og:title"]/@content').get()
        text = '\n'.join(response.css('.endless__item.m-active .article__text ::text').getall())
        keywords = response.xpath('//meta[@name="keywords"]/@content').get()

        yield {
            'title': title,
            'text': text,
            'keywords': keywords
        }

        for next_page in response.css('a.recommend__item-title'):
            yield response.follow(next_page, self.parse)
