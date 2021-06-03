import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import SuperjobItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response:HtmlResponse):
        vacancies_links = response.xpath("//div[@class='_1h3Zg _2rfUm _2hCDz _21a7u']//@href").extract()
        next_page = response.xpath("//a[contains(@class, 'Dalshe')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response:HtmlResponse):
        name = response.css("h1::text").extract_first()
        salary = response.xpath("//span[@class='_1h3Zg _2Wp8I _2rfUm _2hCDz']/text()").extract()
        yield SuperjobItem(name=name, salary=salary)
