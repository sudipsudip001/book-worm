from pathlib import Path
import scrapy
from datetime import date

class bookworm(scrapy.Spider):
    name = "bookworm"
    start_urls = [
        "https://books.toscrape.com/",
    ]

    def parse(self, response):
        for book in response.css("li.col-xs-6.col-sm-4.col-md-3.col-lg-3"):
            url = book.css("a::attr(href)").get()
            yield response.follow(url, callback=self.bookData, meta={"urlData": url})
        # handle pagination
        # next_link = response.css("li.next a").get()
        next_link = response.css("li.next a::attr(href)").get()
        yield response.follow(next_link, callback=self.parse)
        
    def bookData(self, response):
        """
            Collects the required information of each book from the given page and
            returns the data back to the parse method.
        """
        name = response.css("div.col-sm-6.product_main h1::text").get()
        price = response.css("div.col-sm-6.product_main p.price_color::text").get()
        url = response.meta["urlData"]
        date_today = date.today().isoformat()
        description = response.css("article.product_page p")[3].get()[3:-4]
        tax = response.css("table.table.table-striped tr td::text")[4].get()
        availability = response.css("table.table.table-striped tr td::text")[5].get()
        upc = response.css("table.table.table-striped tr td::text")[0].get()
        rating = response.css("div.col-sm-6.product_main p::attr(class)")[2].get().split(' ')[1]

        yield {
            "name": name,
            "url": url,
            "scrape_date": date_today,
            "description": description,
            "price": price,
            "tax": tax,
            "availability": availability,
            "upc": upc,
            "rating": rating
        }

