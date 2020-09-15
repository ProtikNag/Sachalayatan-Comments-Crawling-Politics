from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup


class CommentsSpider(CrawlSpider):
    name = 'sachalayatan'
    allowed_domains = ['www.sachalayatan.com']
    start_urls = []
    my_base_url = 'http://www.sachalayatan.com/লেখার_ধরন/খবর/রাজনীতি?page='

    for i in range(80):
        start_urls.append(my_base_url + str(i))

    rules = (
        Rule(LinkExtractor(allow='/*/[0-9][0-9][0-9][0-9][0-9]#comments', ), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        comments = response.xpath("//div[@class='comment  clear-block language-bn']/div[@class='content']").getall()

        cleantext = []
        for comment in comments:
            soup = BeautifulSoup(comment)
            text = soup.get_text().strip()
            cleantext.append(text)

        with open('../file.txt', 'a') as f:
            for txt in cleantext:
                f.write(txt)
                f.write('\n\n\n')

        yield {
            "Comment": cleantext
        }
