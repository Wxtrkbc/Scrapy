import scrapy
import json
from scrapy.http.request import Request
from scrapy.http import FormRequest
from scrapy.selector import Selector
from songs import settings
from pprint import pprint


class SongSpider(scrapy.Spider):
    name = 'jp'
    allowed_domains = ['www2.jasrac.or.jp']
    start_urls = [
        settings.POST_URL
    ]

    def start_requests(self):
        for name, authors in _generate_search_data().items():
            yield FormRequest(
                self.start_urls[0],
                headers=settings.POST_HEADERS,
                formdata=_generate_query_params_dict(name, authors),
                cookies=settings.DEFAULT_COOKIES
            )

    def parse(self, response):
        # ['main.jsp?trxID=F20101&WORKS_CD=1I711549&subSessionID=001&subSession=start']
        print(response.xpath("//tr/td/a/@href").extract())


def _generate_query_params_dict(name, author):
    settings.DEFAULT_QUERY_PARAMS['IN_WORKS_TITLE_NAME1'] = name
    author_list = author.split(';')
    settings.DEFAULT_QUERY_PARAMS['IN_ARTIST_NAME1'] = author_list[0]
    if 2 == len(author_list):
        settings.DEFAULT_QUERY_PARAMS['IN_ARTIST_NAME_CONDITION'] = 1
        settings.DEFAULT_QUERY_PARAMS['IN_ARTIST_NAME2'] = author_list[1]
    for k, v in settings.DEFAULT_QUERY_PARAMS.items():
        settings.DEFAULT_QUERY_PARAMS[k] = str(v)
    return settings.DEFAULT_QUERY_PARAMS


def _generate_search_data():
    with open('test_data.json') as f:
        test_data = json.load(f)
        return test_data
