import scrapy
import xpinyin
from ..items import PiaohuaMovieItem


class DySpider(scrapy.Spider):
    name = 'dy'
    # allowed_domains = ['piaohua.com']
    start_urls = ['https://www.piaohua.com/']
    base_http = 'https://www.piaohua.com'
    base_type = 'https://www.piaohua.com/html/{}/'

    def __init__(self):
        super(DySpider, self).__init__()
        self.pinyin = xpinyin.Pinyin()

    def parse(self, response):
        type_urls = response.xpath('//div[@class="wp"]/ul/li/a/@href').getall()
        types = response.xpath('//div[@class="wp"]/ul/li/a/text()').getall()
        for url, typ in zip(type_urls, types):
            # print(url)
            meta = {'movie_type': typ}
            yield scrapy.Request(url=self.base_http + url, meta=meta, callback=self.parse_list)

    def parse_list(self, response):
        movie_type = response.meta['movie_type']
        movie_urls = response.xpath('//div[@class="txt"]/h3/a/@href').getall()
        # print('movie_type: ', movie_type)
        for url in movie_urls:
            # print(url)
            yield scrapy.Request(url=self.base_http + url, meta=response.meta, callback=self.parse_detail)
        type_eng = self.pinyin.get_pinyin(movie_type[:2]).replace('-', '')
        print('type_eng::::: ', type_eng)

        next_pages = response.xpath('//div[@class="pages"]/ul/li/a/@href').getall()
        for next_page in next_pages:
            if 'java' not in next_page:
                if 'zongyi' in type_eng:
                    type_eng = 'zongyijiemu'
                yield scrapy.Request(url=self.base_type.format(type_eng) + next_page, meta=response.meta,
                                     callback=self.parse_list)

    def parse_detail(self, response):

        item = PiaohuaMovieItem()
        movielist = response.xpath('//div[@class="m-text1"]/div[@class="bot"]/a/text()').getall()
        if len(movielist) > 0:
            pass
        quanjilist = response.xpath('//div[@class="m-text1"]//table//a/@href').getall()
        if len(quanjilist)>0:
            pass
        name = response.xpath('//div[@class="m-text1"]/h1/text()').get()
        pianming = response.xpath('//div[@class="m-text1"]/div[@class="info"]/span[1]/text()').get()
        release_time = response.xpath('//div[@class="m-text1"]/div[@class="info"]/span[2]/text()').get()

        item['movie_list'] = movielist
        item['quanjilist'] = quanjilist
        item['name'] = name
        item['pianming'] = pianming
        item['release_time'] = release_time

        yield item


