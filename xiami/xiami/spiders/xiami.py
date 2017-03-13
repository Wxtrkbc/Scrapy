# coding: utf-8

import scrapy
import json

from scrapy.http.request import Request
from scrapy.utils.project import get_project_settings
from pprint import pprint
from xiami import settings
from collections import namedtuple, OrderedDict


# settings = get_project_settings()


class SongSpider(scrapy.Spider):
    name = 'xiami'
    allowed_domains = ['http://www.xiami.com/']
    start_urls = [
        # 'http://www.xiami.com/chart/data?c=101&type=1&page=1&limit=10&_=1489373183480',  # 华语
        'http://www.xiami.com/chart/data?c=101&type=2&page=1&limit=10&_=1489373255985',  # 欧美
        # 'http://www.xiami.com/chart/data?c=101&type=3&page=1&limit=200&_=1489373380493',  # 日本
        # 'http://www.xiami.com/chart/data?c=101&type=4&page=1&limit=200&_=1489373475758',   # 韩国

    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url,
                # headers=settings.HEADERS,
                # cookies=settings.DEFAULT_COOKIES,
                callback=self.parse,
            )

    def parse(self, response):
        td_songs = response.xpath("//td[@class='songblock']")
        rep_dict = _generate_song_info_dict_from_tds(td_songs)
        with open('../songs/song_data.json', 'a+') as f:
            json.dump(rep_dict, f)


def _generate_song_info_dict_from_tds(tds):
    song_info = namedtuple('Song', ['name', 'authors'])  # just for fun
    rep_dict = OrderedDict()
    for td in tds:
        song_info.name = td.xpath(".//strong//a/text()").extract()[0]
        authors = td.xpath(".//a[@class='artist']/text()").extract()
        song_info.authors = ';'.join(authors)
        rep_dict[song_info.name] = song_info.authors
    return rep_dict


