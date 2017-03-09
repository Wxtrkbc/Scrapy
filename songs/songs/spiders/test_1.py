# coding: utf-8

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
        # pbody = body.replace('&nbsp;', ' ')
        # tds = Selector(text=body).xpath('//td')
        # data = to_native_str(response.body).replace('&nbsp;', ' ')
        # print(data)
        # response = Selector(text=data)
        trs = response.xpath('//body/table[@class="contentsTable"]/tr')
        data_list = [0] * len(trs)
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
            data_list[index] = temp
        print(data_list)

    def parse_url(self, response):
        # ['main.jsp?trxID=F20101&WORKS_CD=1I711549&subSessionID=001&subSession=start']
        params = response.xpath("//tr/td/a/@href").extract()
        for param in params:
            print(settings.GET_URL + param, '-------------')
            yield Request(
                settings.GET_URL + param,
                headers=settings.HEADERS,
                cookies=settings.DEFAULT_COOKIES,
                callback=self.parse,
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


# from scrapy.selector import Selector
# from scrapy.http import HtmlResponse
#
# body = '<th class="lightTitleMMs" nowrap>No.</th><th class="lightTitleMMs" nowrap><a href="help/help_words.html#societyorganization" target="_blank">Š‘®’c‘Ì</a></th><th class="darkTitleMMs"  nowrap><img alt="JASRAC‚ª’˜ìŒ ‚ðŠÇ—‚µ‚Ä‚¢‚Ü‚·iˆê•”ŠÇ—‚ðŠÜ‚ÞjB‚²—˜—p‚ÌÛ‚ÍAJASRAC‚Ì‹–‘ø‚ª•K—v‚Å‚·B" border="0" src="img/management_icon_J.png" title="JASRAC‚ª’˜ìŒ ‚ðŠÇ—‚µ‚Ä‚¢‚Ü‚·iˆê•”ŠÇ—‚ðŠÜ‚ÞjB‚²—˜—p‚ÌÛ‚ÍAJASRAC‚Ì‹–‘ø‚ª•K—v‚Å‚·B"></th>'
#
# ths = Selector(text=body).xpath('//th')
#
# for th in ths:
#     if th.xpath('.//img'):
#         print(th.xpath('.//img/@src').extract()[0])
#     else:
#         print(th.xpath('.//text()').extract()[0])

# from scrapy.selector import Selector
# from scrapy.http import HtmlResponse
#
body = """
    <td valign="middle" class="&nbsp;">
        <div align="center" class="&nbsp;">1</div>
    </td>
    <td valign="middle" class="&nbsp;">
        <!-- <span class="&nbsp;" style="margin-right: 5px;">00535020593</span> -->
        <span class="&nbsp;">BORGEN JESPER</span>
    </td>
    <td valign="middle" class="&nbsp;" nowrap>
        <div align="center" class="&nbsp;">ì‹ÈìŽŒ</div>
    </td>
    <td valign="middle" class="&nbsp;" nowrap>
        <div align="center" class="&nbsp;">&nbsp;</div>
    </td>
    <td valign="middle" class="&nbsp;" nowrap>
        <div align="center" class="&nbsp;">‰‰˜^M</div>
    </td>
    <td valign="middle" class="&nbsp;" nowrap>
        <div align="center" class="&nbsp;">‰‰:TONO&nbsp;˜^:NCB</div>
    </td>
    <td valign="middle" class="lightTitleMMs">&nbsp;</td>
    <td valign="middle" class="lightTitleMMs">&nbsp;</td>
    <td valign="middle" class="lightTitleMMs">&nbsp;</td>
    <td valign="middle" class="lightTitleMMs">&nbsp;</td>
    <td valign="middle" class="lightTitleMMs">&nbsp;</td>
    <td valign="middle" class="lightTitleMMs">&nbsp;</td>
    <td valign="middle" class="lightTitleMMs">&nbsp;</td>
    <td valign="middle" class="lightTitleMMs">&nbsp;</td>
    <td valign="middle" class="lightTitleMMs">&nbsp;</td>
    <td valign="middle" class="lightTitleMMs">&nbsp;</td>
    <td valign="middle" class="lightTitleMMs">
        <img alt="“–ŠYŽx•ªŒ E—˜—pŒ`‘Ô‚É‚Â‚¢‚Ä‚ÍAJASRAC‚ÉŠÇ—‚ðˆÏ‘õ‚µ‚Ä‚¢‚È‚¢Œ —˜ŽÒ‚Å‚·B‚½‚¾‚µA•¡‡Œ i•ú‘—E”zME’ÊƒJƒ‰j‚É‚Â‚¢‚Ä‚ÍAˆê•”‚ÌŽx•ªŒ ‚ÌŠÇ—‚ð‚µ‚Ä‚¢‚éê‡‚ª‚ ‚è‚Ü‚·B" border="0" src="img/management_icon_sharp.png" title="“–ŠYŽx•ªŒ E—˜—pŒ`‘Ô‚É‚Â‚¢‚Ä‚ÍAJASRAC‚ÉŠÇ—‚ðˆÏ‘õ‚µ‚Ä‚¢‚È‚¢Œ —˜ŽÒ‚Å‚·B‚½‚¾‚µA•¡‡Œ i•ú‘—E”zME’ÊƒJƒ‰j‚É‚Â‚¢‚Ä‚ÍAˆê•”‚ÌŽx•ªŒ ‚ÌŠÇ—‚ð‚µ‚Ä‚¢‚éê‡‚ª‚ ‚è‚Ü‚·B">
    </td>
    <td valign="middle" class="lightTitleMMs">
        <img alt="“–ŠYŽx•ªŒ E—˜—pŒ`‘Ô‚É‚Â‚¢‚Ä‚ÍAJASRAC‚ÉŠÇ—‚ðˆÏ‘õ‚µ‚Ä‚¢‚È‚¢Œ —˜ŽÒ‚Å‚·B‚½‚¾‚µA•¡‡Œ i•ú‘—E”zME’ÊƒJƒ‰j‚É‚Â‚¢‚Ä‚ÍAˆê•”‚ÌŽx•ªŒ ‚ÌŠÇ—‚ð‚µ‚Ä‚¢‚éê‡‚ª‚ ‚è‚Ü‚·B" border="0" src="img/management_icon_sharp.png" title="“–ŠYŽx•ªŒ E—˜—pŒ`‘Ô‚É‚Â‚¢‚Ä‚ÍAJASRAC‚ÉŠÇ—‚ðˆÏ‘õ‚µ‚Ä‚¢‚È‚¢Œ —˜ŽÒ‚Å‚·B‚½‚¾‚µA•¡‡Œ i•ú‘—E”zME’ÊƒJƒ‰j‚É‚Â‚¢‚Ä‚ÍAˆê•”‚ÌŽx•ªŒ ‚ÌŠÇ—‚ð‚µ‚Ä‚¢‚éê‡‚ª‚ ‚è‚Ü‚·B">
    </td>

"""
# # pbody = body.replace('&nbsp;', ' ')
# body_bytes = bytes(body, encoding='utf-8')
# print(type(body_bytes), str(body_bytes, encoding='utf-8'))
# tds = Selector(text=body).xpath('//td')
#
# for td in tds:
#     if td.xpath('.//span'):
#         print(td.xpath('.//span/text()').extract()[0])
#     elif len(td.xpath('.//div')):
#         print(td.xpath('.//div/text()').extract()[0])
#     else:
#         print(td.xpath('.//img/@src').extract()[0] if td.xpath('.//img/@src') else None)
