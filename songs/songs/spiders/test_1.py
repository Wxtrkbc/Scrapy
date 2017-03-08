import scrapy
from scrapy.http.request import Request
from scrapy.selector import Selector

class SongSpider(scrapy.Spider):

    name = 'jp'
    allowed_domains = ['www2.jasrac.or.jp']
    start_urls = [
        'http://www2.jasrac.or.jp/eJwid/main.jsp?trxID=F20101&WORKS_CD=7D156098&subSessionID=001&subSession=start'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={
                'JSESSIONID': 'L-yPn8PiASo7RWge9a3IuseJ',
                'BIGipServerpool_eJwid': '3256656394.21504.0000',
                '_ga': 'GA1.3.220186252.1488880843'
            })

    def parse(self, response):
        print response.body

