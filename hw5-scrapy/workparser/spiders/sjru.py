import scrapy
from workparser.items import WorkparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response):
        next_page = response.css('a.f-test-link-dalshe::attr(href)').extract_first() #Ссылка на след. страницу
        if not next_page:
            pass
        else:
            yield response.follow(next_page, callback=self.parse)

        vacansy = response.css(
            'div.f-test-vacancy-item a[target="_blank"]::attr(href)').extract()

        for link in vacansy:
            yield response.follow(link, self.vacansy_parse)  # Переходим на страницы вакансий

    # Тут будем передавать только min_salary как массив из кусков текста и далее трансформируем его в pipeline
    def vacansy_parse(self, response):
        name = response.css('h1::text').extract_first()
        salary = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']").extract()
        link = response.css('link[rel="canonical"]::attr(href)').extract_first()
        yield WorkparserItem(name=name, salary = salary, salary_min=None, salary_max=None, link=link, resource='sj')




