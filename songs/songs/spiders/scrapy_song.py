# coding: utf-8

import scrapy
import json
import csv
from scrapy.http.request import Request
from scrapy.http import FormRequest
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
                headers=settings.HEADERS,
                formdata=_generate_query_params_dict(name, authors),
                cookies=settings.DEFAULT_COOKIES,
                callback=self.parse_url,
                meta={
                    "name": name,
                    "authors": authors
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
            data_list[index+1] = temp
        data_list[0] = [song_info]
        _change_to_csv('data.csv', data_list)

    def parse_url(self, response):
        # ['main.jsp?trxID=F20101&WORKS_CD=1I711549&subSessionID=001&subSession=start']
        params = response.xpath("//tr/td/a/@href").extract()
        for param in params:
            yield Request(
                settings.GET_URL + param,
                headers=settings.HEADERS,
                cookies=settings.DEFAULT_COOKIES,
                callback=self.parse,
                meta=response.meta
            )


def _generate_query_params_dict(name, author):
    settings.DEFAULT_QUERY_PARAMS['IN_WORKS_TITLE_NAME1'] = name
    author_list = author.split(';')
    settings.DEFAULT_QUERY_PARAMS['IN_ARTIST_NAME1'] = author_list[0]
    if 2 == len(author_list):
        settings.DEFAULT_QUERY_PARAMS['IN_ARTIST_NAME_CONDITION'] = str(1)
        settings.DEFAULT_QUERY_PARAMS['IN_ARTIST_NAME2'] = author_list[1]
    return settings.DEFAULT_QUERY_PARAMS


def _generate_search_data():
    # with open('../../test_data.json') as f:
    with open('test_data.json') as f:
        test_data = json.load(f)
        return test_data


def _format_first_ths(ths):
    th_list = []
    for th in ths:
        if th.xpath('.//span'):
            th_list.append(th.xpath('.//span/text()').extract()[0])
        else:
            th_list.append(th.xpath('.//text()').extract()[0])

    return _fill_none_str_for_th(th_list)


def _format_other_ths(ths):
    th_list = []
    for th in ths:
        if th.xpath('.//img'):
            th_list.append(th.xpath('.//img/@src').extract()[0])
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
            td_list.append(td.xpath('.//img/@src').extract()[0] if td.xpath('.//img/@src') else ' ')
    return td_list


def _change_to_csv(file_name, data_list):
    with open(file_name, 'a', encoding='utf-8') as cf:
        csv_writer = csv.writer(cf)
        for data in data_list:
            csv_writer.writerow(data)


def _fill_none_str_for_th(th_list):
    for i in range(3):
        th_list.insert(1, ' ')
    for i in range(2):
        th_list.insert(5, ' ')
    return th_list
