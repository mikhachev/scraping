from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avitoautoparser.spiders.avito import AvitoAutoSpider
from avitoautoparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoAutoSpider)
    process.start()
