from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
from blog_crawlin.utils import create_csv
from datetime import date


class CommentsSpider(CrawlSpider):
    name = 'sachalayatan'
    allowed_domains = ['www.sachalayatan.com']
    start_urls = []
    my_base_url = 'http://www.sachalayatan.com/লেখার_ধরন/খবর/রাজনীতি?page='
    id = 0
    category = 'Politics'
    doc_type = 'Undefined'
    root_url = 'http://www.sachalayatan.com/লেখার_ধরন/খবর/রাজনীতি'
    data_source = 'Blog'
    url = None
    published_date = None
    scraped_date = date.today()
    domain = 'www.sachalayatan.com'


    for i in range(80):
        start_urls.append(my_base_url + str(i))

    rules = (
        Rule(LinkExtractor(allow='/*/[0-9][0-9][0-9][0-9][0-9]#comments', ), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        comments = response.xpath("//div[@class='comment  clear-block language-bn']/div[@class='content']").getall()
        date_text = response.xpath("//div[@class='comment  clear-block language-bn']/div[@class='submitted']").getall()

        cleantext = []
        for comment in comments:
            soup = BeautifulSoup(comment)
            text = soup.get_text().strip()
            cleantext.append(text)

        cleandate = []
        for dt in date_text:
            soup = BeautifulSoup(dt)
            strip_date = soup.get_text().strip()
            date = strip_date.split("তারিখ:")[1][:-1]
            cleandate.append(date)

        self.url = response.url

        for i in range(len(cleantext)):
            id = self.id + 1
            self.id += 1
            text = cleantext[i]
            category = self.category
            doc_type = self.doc_type
            root_url = self.root_url
            data_source = self.data_source
            url = self.url
            published_date = cleandate[i]
            scraped_date = self.scraped_date
            domain = self.domain

            ret = [id, text, category, doc_type, root_url, data_source, url, published_date, scraped_date, domain]

            create_csv(ret)

        yield {}
