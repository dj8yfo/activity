import logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from morphs.spiders.mimics import MimicSpider
import sys


configure_logging({'LOG_FORMAT': '%(module)s %(levelname)s: %(message)s'},
                  install_root_handler=False)
logging.basicConfig(
    filename='log_scrape.log',
    format='%(module)s | %(levelname)s: %(message)s',
    level=logging.DEBUG
)
settings = get_project_settings()

runner = CrawlerRunner(settings)

if len(sys.argv) > 1:
    start_arg = int(sys.argv[1])
else:
    start_arg = 0
print(f"start index for parsing: {start_arg}")


for location in ('ny', 'sf', 'la'):
    for category in ('gyms', 'spas', 'restaurants'):
        if category == 'restaurants':
            per_page = 30
        else:
            per_page = 10
        runner.crawl(MimicSpider, cat=category, loc=location, per_page=per_page, start=start_arg)

d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
