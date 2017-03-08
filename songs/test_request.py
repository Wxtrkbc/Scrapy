import requests

request_url = 'http://www2.jasrac.or.jp/eJwid/main.jsp'
payload = {'trxID': 'A00401-3'}

headers = {
    'Cookie': 'JSESSIONID=L-yPn8PiASo7RWge9a3IuseJ; BIGipServerpool_eJwid=3256656394.21504.0000;'
              ' _ga=GA1.3.220186252.1488880843',
    # 'Host': 'www2.jasrac.or.jp',
    # 'Origin': 'http://www2.jasrac.or.jp',
    # 'Referer': 'http://www2.jasrac.or.jp/eJwid/main.jsp?trxID=A00401-2',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 '
    #               '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

data = {
    "IN_DEFAULT_WORKS_KOUHO_MAX": 20,
    "IN_DEFAULT_WORKS_KOUHO_SEQ": 1,
    "IN_WORKS_TITLE_OPTION1": 0,
    "IN_WORKS_TITLE_NAME1": "City of Stars",
    "IN_WORKS_TITLE_TYPE1": 0,
    "IN_WORKS_TITLE_CONDITION": 0,
    "IN_WORKS_TITLE_OPTION2": 0,
    "IN_WORKS_TITLE_TYPE2": 0,
    "IN_KEN_NAME_OPTION1": 0,
    "IN_KEN_NAME_JOB1": 0,
    "IN_KEN_NAME_CONDITION": 0,
    "IN_KEN_NAME_OPTION2": 0,
    "IN_KEN_NAME_JOB2": 0,
    "IN_ARTIST_NAME_OPTION1": 0,
    "IN_ARTIST_NAME1": "Ryan Gosling",
    "IN_ARTIST_NAME_CONDITION": 1,
    "IN_ARTIST_NAME_OPTION2": 0,
    "IN_ARTIST_NAME2": "Emma Stone",
    "IN_DEFAULT_SEARCH_WORKS_NAIGAI": 0,
    "RESULT_CURRENT_PAGE": 1
}

r = requests.post(request_url, data=data, headers=headers, params=payload)
print r, r.status_code, r.text
