import scrapy
import logging
from fuse_transmute.boutiques import GoPostalMode, Boutique

URLPATTERN_FILE = '0ck2cj9LPpV.snip'
with open(URLPATTERN_FILE, 'r') as f:
    TEMPLATE_URL = f.read()
INDILINK = "a[href^='/biz'][name]:not([name=''])"


class MimicSpider(scrapy.Spider):
    name = 'swap-fledge'
    start = 0
    upper_limit = 1000  # 1000

    def start_requests(self):
        if getattr(self, 'cat', None) is None or \
                getattr(self, 'loc', None) is None or \
                getattr(self, 'per_page', None) is None:
            raise Exception('provide category <cat> , location <loc> '
                            'and <per_page> args')

        # start_url = TEMPLATE_URL.format(cat=self.cat, loc=self.loc, start=self.start)
        # yield scrapy.Request(url=start_url, callback=self.entry_point)

        per_page = int(self.per_page)
        yield from self.main_cycle(per_page)

    def main_cycle(self, per_page):
        for start_index in range(self.start, self.upper_limit, per_page):
            url = TEMPLATE_URL.format(cat=self.cat, loc=self.loc, start=start_index)
            yield scrapy.Request(url=url, callback=self.parse_list_page)

    def entry_point(self, response):
        subpages = response.css(INDILINK)
        per_page = len(subpages)
        self.log(f'found {per_page} subresults at entry point', level=logging.INFO)
        yield from self.main_cycle(per_page)

    def parse_list_page(self, response):
        self.log(f'visited page {response.urljoin("")}', level=logging.INFO)

        sublinks = response.css(INDILINK)
        # sanity check the page has actually been downloaded
        if not sublinks:
            yield scrapy.Request(url=response.url, dont_filter=True,
                                 callback=self.parse_list_page)

        for link in sublinks:
            yield response.follow(link, callback=self.parse_biz_page)

    def parse_biz_page(self, response):
        self.log(f'visited buziness page {response.urljoin("")}', level=logging.INFO)
        address_sel = 'address p span::text'

        # sanity check the page has actually been downloaded
        address_elements = response.css(address_sel).getall()
        if not address_elements:
            yield scrapy.Request(url=response.url, dont_filter=True,
                                 callback=self.parse_biz_page)

        phone_xpath = "//p[contains(.,'Phone')]/following-sibling::p[1]/text()"
        images_xpath = "//div[contains(@class, 'photo-header-media')]//img"
        reviews_xpath = \
            "//a[contains(@class, 'rating-detail')]/ancestor::*[5]" +\
            "//p[contains(., 'review')]/text()"
        about_xpath = \
            "//h3[contains(., 'About the Business')]/ancestor::section[1]//text()"
        website_elements = response.xpath("//a[contains(@href, '/biz_redir?url')]")
        image_elements = response.xpath(images_xpath)
        image_element_attrib = image_elements[0].attrib if image_elements else {}
        res = {
            'url': response.url,
            'addresses': address_elements,
            'title': response.css('h1[class*="heading"]::text').get(),
            'phone': response.xpath(phone_xpath).get(),
            'category': self.cat,
            'image_url_raw': image_element_attrib.get('src', ''),
            'reviews_str': response.xpath(reviews_xpath).get() or '',
            'website_raw': website_elements.attrib.get('href', ''),
            'schedule_raw': ('| '.join(response.xpath("//table/tbody//text()").getall())).
            replace('\n', '| '),

            'about_raw': (' '.join(response.xpath(about_xpath).getall())).replace('\n', ' ')
        }
        yield {
            'boutique': Boutique.from_kadmin(res),
            'postal': GoPostalMode.from_kadmin(res)
        }
