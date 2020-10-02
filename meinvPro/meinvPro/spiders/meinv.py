import scrapy
from meinvPro.items import MeinvproItem


class MeinvSpider(scrapy.Spider):
    name = 'meinv'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://pic.netbian.com/4kdongwu/']

    url = 'http://pic.netbian.com/4kdongwu/index_%d.html'
    page_num = 2

    # 解析详情页数据
    def parse_detail(self, response):
        item = response.meta['item']
        img_name = response.xpath('//*[@id="main"]/div[2]/div[1]/div[1]/h1/text()').extract_first()
        img_size = response.xpath('//*[@id="main"]/div[2]/div[2]/div[2]/p[3]/span/text() | //*[@id="main"]/div[2]/div[2]/div[3]/p[3]/span/text()').extract_first()
        item['img_name'] = img_name
        item['img_size'] = img_size
        yield item

    # 解析首页
    def parse(self, response):
        li_list = response.xpath('//*[@id="main"]/div[3]/ul/li')

        for li in li_list:
            img_href = 'http://pic.netbian.com' + li.xpath('./a/@href').extract_first()
            img_src = 'http://pic.netbian.com' + li.xpath('./a/img/@src').extract_first()

            item = MeinvproItem()  # 一条数据对应一个对象
            item['img_src'] = img_src
            yield scrapy.Request(url=img_href, callback=self.parse_detail, meta={'item':item})  # 请求传参

        # 分页爬取
        if self.page_num <= 20:
            new_url = format(self.url%self.page_num)
            self.page_num += 1
            yield scrapy.Request(url=new_url, callback=self.parse)