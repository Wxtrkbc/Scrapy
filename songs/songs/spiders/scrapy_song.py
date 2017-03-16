# coding: utf-8

import scrapy
import json
import csv
import random
import time

from scrapy.http.request import Request
from scrapy.http import FormRequest
from songs import settings
from pprint import pprint

from songs.spiders.pinyin import PinYin
from songs.spiders.langconv import *

PROXIES = [
    {'ip_port': '115.28.168.247:80'},
    {'ip_port': '203.91.121.74:3128'},
    {'ip_port': '124.207.132.242:3128'},
    {'ip_port': '124.234.157.250:80'},
    {'ip_port': '218.241.181.202:8080'},
]
DOWNLOAD_DELAY = 1

# http://www2.jasrac.or.jp/eJwid/help/help_words.html#iswc
_map_rights = {
    'img/management_icon_J.png': 'V',
    'img/management_icon_batsu.png': 'X',
    'img/management_icon_sharp.png': '#',
    'img/management_icon_hyphen.png': '-',
    'img/management_icon_confirmation.png': '确认',
    'img/management_icon_lapse.png': '消失',
    'img/management_icon_lapse_pd.png': '消失',
    'img/management_icon_undecided.png': '未确定',
    'img/management_icon_exclusive.png': '专属',
}


class SongSpider(scrapy.Spider):
    name = 'jp'
    allowed_domains = ['www2.jasrac.or.jp']
    start_urls = [
        settings.POST_URL
    ]

    # 汉字转拼音
    pinyin = PinYin()
    pinyin.load_word()

    def start_requests(self):
        for name, authors in _generate_search_data(self.pinyin).items():
            time.sleep(DOWNLOAD_DELAY)
            proxy = random.choice(PROXIES)
            yield FormRequest(
                self.start_urls[0],
                headers=settings.HEADERS,
                formdata=_generate_query_params_dict(name, authors),
                cookies=settings.DEFAULT_COOKIES,
                callback=self.parse_url,
                meta={
                    "name": name,
                    "authors": authors,
                    "proxy": "http://{}".format(proxy['ip_port']),
                    "proxy_item": proxy
                }
            )

    def parse(self, response):
        trs = response.xpath('//body/table[@class="contentsTable"]/tr')
        song_info = response.meta['name'] + '--' + response.meta['authors']
        data_list = [0] * (len(trs) + 1)
        for index, item in enumerate(trs):
            temp = None
            if index < 1:
                ths = item.xpath('.//th')
                temp = _format_first_ths(ths)
            elif index == 1:
                ths = item.xpath('.//th')
                temp = _format_other_ths(ths)
            else:
                tds = item.xpath('.//td')
                temp = _format_tds(tds)
            data_list[index + 1] = temp
        data_list[0] = [song_info]
        _change_to_csv('data.csv', data_list)

    def parse_url(self, response):
        # ['main.jsp?trxID=F20101&WORKS_CD=1I711549&subSessionID=001&subSession=start']
        if response.status == 403:
            proxy_id = PROXIES.index(response.meta['proxy_item'])
            del PROXIES[proxy_id]
            return None
        params = response.xpath("//tr/td/a/@href").extract()
        print(params, 'xxxx')
        for param in params:
            time.sleep(DOWNLOAD_DELAY)
            yield Request(
                settings.GET_URL + param,
                headers=settings.HEADERS,
                cookies=settings.DEFAULT_COOKIES,
                callback=self.parse,
                meta=response.meta
            )


def _generate_query_params_dict(name, author):
    settings.DEFAULT_QUERY_PARAMS['IN_WORKS_TITLE_NAME1'] = name
    if '(' in author:
        author = author.replace('(', ';').replace(')', '')
    author_list = author.split(';')
    settings.DEFAULT_QUERY_PARAMS['IN_ARTIST_NAME1'] = _format_author_name(author_list[0])
    if 2 == len(author_list):
        settings.DEFAULT_QUERY_PARAMS['IN_ARTIST_NAME_CONDITION'] = str(1)
        settings.DEFAULT_QUERY_PARAMS['IN_ARTIST_NAME2'] = _format_author_name(author_list[1])
    return settings.DEFAULT_QUERY_PARAMS


def _generate_search_data(converter):
    # with open('../../test_data.json') as f:
    with open('test_data.json') as f:
        test_data = json.load(f)
        # 歌名转拼音， 歌手转换繁体
        print({str(converter.hanzi2pinyin_split(string=k, split='').upper()): Converter(
            'zh-hant').convert(v) for k, v in test_data.items()})

        return {str(converter.hanzi2pinyin_split(string=k, split='').upper()): Converter(
            'zh-hant').convert(v) for k, v in test_data.items()}
        # return test_data


def _format_first_ths(ths):
    th_list = []
    for th in ths:
        if th.xpath('.//span'):
            th_list.append(th.xpath('.//span/text()').extract()[0])
        else:
            th_list.append(th.xpath('.//text()').extract()[0])

    return _fill_null_str_for_th(th_list)


def _format_other_ths(ths):
    th_list = []
    for th in ths:
        if th.xpath('.//img'):
            th_list.append(_map_rights[th.xpath('.//img/@src').extract()[0]])
        else:
            th_list.append(th.xpath('.//text()').extract()[0])
    return th_list


def _format_tds(tds):
    td_list = []
    for td in tds:
        if td.xpath('.//span'):
            td_list.append(td.xpath('.//span/text()').extract()[0])
        if td.xpath('.//div'):
            data = td.xpath('.//div/text()').extract()[0]
            td_list.append(data if str(data) != '\xa0' else ' ')
        else:
            td_list.append(_map_rights[td.xpath('.//img/@src').extract()[0]] if td.xpath(
                './/img/@src') else ' ')
    return td_list


def _change_to_csv(file_name, data_list):
    with open(file_name, 'a', encoding='utf-8') as cf:
        csv_writer = csv.writer(cf)
        for data in data_list:
            csv_writer.writerow(data)


def _fill_null_str_for_th(th_list):
    for i in range(3):
        th_list.insert(1, ' ')
    for i in range(2):
        th_list.insert(5, ' ')
    return th_list


def _format_author_name(name):
    """
    李多强  ---》  李 多强
    """

    if len(name) == 3:
        name_list = list(name)
        name_list.insert(1, ' ')
        return ''.join(name_list)
    return name
