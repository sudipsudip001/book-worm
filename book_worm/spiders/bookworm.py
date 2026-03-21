from pathlib import Path
import scrapy
from datetime import date

class bookworm(scrapy.Spider):
    name = "bookworm"
    start_urls = [
        "https://books.toscrape.com/",
    ]

    def parse(self, response):
        book_list = response.css("li.col-xs-6.col-sm-4.col-md-3.col-lg-3") or response.xpath("//ol[@class='row']//li[contains(@class, 'col-xs-6')]")
        for book in book_list:
            url = book.css("a::attr(href)").get() or book.xpath("//div[@class='image_container']/a/@href").get()
            yield response.follow(url, callback=self.bookData)
        # handle pagination
        next_link = response.css("li.next a::attr(href)").get() or response.xpath("//li[@class='next']/a/@href").get()
        yield response.follow(next_link, callback=self.parse)

    def bookData(self, response):
        """
            Collects the required information of each book from the given page and
            returns the data back to the parse method.
        """
        name = response.css("div.col-sm-6.product_main h1::text").get() or response.xpath("//div[@class='product_main']/h1/text()").get()
        price = response.css("div.col-sm-6.product_main p.price_color::text").get() or response.xpath("//div[@class='product_main']/p/text()").get()
        date_today = date.today().isoformat()
        description = response.css("article.product_page p")[3].get()[3:-4] or response.xpath("//article[@class='product_page']/p/text()").get()
        tax = response.css("table.table.table-striped tr td::text")[4].get() or response.xpath("//table/tr/td/text()")[4].get()
        availability = response.css("table.table.table-striped tr td::text")[5].get() or response.xpath("//table/tr/td/text()")[5].get()
        upc = response.css("table.table.table-striped tr td::text")[0].get() or response.xpath("//table/tr/td/text()")[0].get()
        rating = response.css("div.col-sm-6.product_main p::attr(class)")[2].get().split(' ')[1] or response.xpath("//div[contains(@class, 'col-sm-6')]/p/@class").getall()[2].split()[1]

        yield {
            "name": name if name else None,
            "url": response.url if response.url else None,
            "scrape_date": date_today,
            "description": description if description else None,
            "price": price if price else None,
            "tax": tax if tax else None,
            "availability": availability if availability else None,
            "upc": upc if upc else None,
            "rating": rating if rating else None
        }

