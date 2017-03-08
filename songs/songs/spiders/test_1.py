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
                headers=settings.HEADERS,
                formdata=_generate_query_params_dict(name, authors),
                cookies=settings.DEFAULT_COOKIES,
                callback=self.parse_url
            )

    def parse(self, response):
        trs = response.xpath('//body/table[@class="contentsTable"]/tr')
        data_list = []
        for index, item in enumerate(trs):
            if index < 1:
                ths = item.xpath('.//th')
                th_list = _format_first_ths(ths)
                print(th_list)
            if index ==1:
                ths = item.xpath('.//th')
                th_list = _format_other_ths(ths)
                print(th_list)
            else:




    def parse_url(self, response):
        # ['main.jsp?trxID=F20101&WORKS_CD=1I711549&subSessionID=001&subSession=start']
        params = response.xpath("//tr/td/a/@href").extract()
        for param in params:
            print(settings.GET_URL + param, '-------------')
            yield Request(
                settings.GET_URL + param,
                headers=settings.HEADERS,
                cookies=settings.DEFAULT_COOKIES,
                callback=self.parse
            )


def _generate_query_params_dict(name, author):
    settings.DEFAULT_QUERY_PARAMS['IN_WORKS_TITLE_NAME1'] = name
    author_list = author.split(';')
    settings.DEFAULT_QUERY_PARAMS['IN_ARTIST_NAME1'] = author_list[0]
    if 2 == len(author_list):
        settings.DEFAULT_QUERY_PARAMS['IN_ARTIST_NAME_CONDITION'] = 1
        settings.DEFAULT_QUERY_PARAMS['IN_ARTIST_NAME2'] = author_list[1]
    return settings.DEFAULT_QUERY_PARAMS


def _generate_search_data():
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
    return th_list


def _format_other_ths(ths):
    th_list = []
    for th in ths:
        if th.xpath('.//img'):
            th_list.append(th.xpath('.//img/@src').extract()[0])
        else:
            th_list.append(th.xpath('.//text()').extract()[0])
    return th_list

# from scrapy.selector import Selector
# from scrapy.http import HtmlResponse
#
# body = '<th class="darkTitleMM" colspan="4">Œ —˜ŽÒî•ñ</th><th class="darkTitleMM" colspan="2"><a href="help/help_words.html#right" target="_blank">ŠÇ-ó‹µ</a></th><th class="darkTitleMM"><span style="color:#ffff00;">‰‰‘t</span></th>'
#
#
# ths = Selector(text=body).xpath('//th')
# str = ''
# for i in ths:
#     if i.xpath('.//span'):
#         print(i.xpath('.//span/text()').extract()[0])
#     else:
#         print(i.xpath('.//text()').extract()[0])


from scrapy.selector import Selector
from scrapy.http import HtmlResponse

body = '<th class="lightTitleMMs" nowrap>No.</th><th class="lightTitleMMs" nowrap><a href="help/help_words.html#societyorganization" target="_blank">Š‘®’c‘Ì</a></th><th class="darkTitleMMs"  nowrap><img alt="JASRAC‚ª’˜ìŒ ‚ðŠÇ—‚µ‚Ä‚¢‚Ü‚·iˆê•”ŠÇ—‚ðŠÜ‚ÞjB‚²—˜—p‚ÌÛ‚ÍAJASRAC‚Ì‹–‘ø‚ª•K—v‚Å‚·B" border="0" src="img/management_icon_J.png" title="JASRAC‚ª’˜ìŒ ‚ðŠÇ—‚µ‚Ä‚¢‚Ü‚·iˆê•”ŠÇ—‚ðŠÜ‚ÞjB‚²—˜—p‚ÌÛ‚ÍAJASRAC‚Ì‹–‘ø‚ª•K—v‚Å‚·B"></th>'

ths = Selector(text=body).xpath('//th')

for th in ths:
    if th.xpath('.//img'):
        print(th.xpath('.//img/@src').extract()[0])
    else:
        print(th.xpath('.//text()').extract()[0])
