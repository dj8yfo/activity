from scrapy.http import TextResponse
from morphs.spiders.mimics import MimicSpider
import requests
import json
mim = MimicSpider(cat='restaurants')

with open('test/cGqBcnDzvC2.snip') as f:
    url = f.read()

resp = requests.get(url=url)
tr = TextResponse(url, body=resp.content)
gener = mim.parse_biz_page(tr)
for x in gener:
    for file, obj in [('test/boutique.json', 'boutique'), ('test/postal.json', 'postal')]:
        with open(file) as file_cont:
            expected = json.loads(file_cont.read())

        actual = x[obj].__dict__
        for key in expected.keys():
            if key == 'website':
                assert 'biz_redir' in actual[key], 'website xpath change'
            elif key == 'reviews':
                assert actual[key] > 5000, 'reviews xpath change'
            elif key == 'schedule':
                assert 'Sun' in actual[key]  # always a Sunday
            else:
                assert expected[key] == actual[key], f'file: {file}; key: {key};' +\
                    f'{expected[key]} exp vs {actual[key]}'
