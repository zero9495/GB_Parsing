import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import LeroymerlinItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super(LeroymerlinSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{query}/']

    def parse(self, response:HtmlResponse):
        goods_links = response.xpath("//a[@data-qa-product-image]/@href").extract()
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in goods_links:
            yield response.follow(link, callback=self.parse_goods)


    def parse_goods(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photos', "//img[@alt='image thumb']/@src | //img[@alt='product image']/@src")
        loader.add_value('link', response.url)
        loader.add_xpath('params', "//dl/div")
        yield loader.load_item()
        # name = response.css("h1::text").extract_first()
        # price = response.xpath("//span[@slot='price']/text()").extract()
        # photos = response.xpath("//img[@alt='image thumb']/@src").extract()
        # if not photos:
        #     photos = response.xpath("//img[@alt='product image']/@src").extract()
        # if not photos:
        #     print()
        # yield LeroymerlinItem(name=name, price=price, photos=photos)
