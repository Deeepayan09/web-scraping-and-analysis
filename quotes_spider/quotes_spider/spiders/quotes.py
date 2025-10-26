# quotes_spider/spiders/quotes.py
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com/"]

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 1.0,
        "AUTOTHROTTLE_ENABLED": True,
        "ITEM_PIPELINES": {
            "quotes_spider.pipelines.CleanPipeline": 300,
            "quotes_spider.pipelines.SaveJsonLinePipeline": 800,
        },
        "USER_AGENT": "Mozilla/5.0 (compatible; DataScraper/1.0; +https://example.com/bot)"
    }

    def parse(self, response):
        for q in response.css(".quote"):
            yield {
                "text": q.css("span.text::text").get(),
                "author": q.css("small.author::text").get(),
                "tags": q.css(".tags a.tag::text").getall(),
            }
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
