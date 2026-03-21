from pathlib import Path
import scrapy
from datetime import date

class bookworm(scrapy.Spider):
    name = "bookworm"
    start_urls = [
        "https://books.toscrape.com/",
    ]

    def parse(self, response):
        try:
            book_list = response.css("li.col-xs-6.col-sm-4.col-md-3.col-lg-3") or response.xpath("//ol[@class='row']//li[contains(@class, 'col-xs-6')]")
            for book in book_list:
                url = book.css("a::attr(href)").get() or book.xpath("//div[@class='image_container']/a/@href").get()
                yield response.follow(url, callback=self.bookData, errback=self.handle_error)
        except Exception:
            print(f"COULDN'T SCRAPE DATA DUE TO FAILURE IN LINK.")
        # handle pagination
        next_link = response.css("li.next a::attr(href)").get() or response.xpath("//li[@class='next']/a/@href").get()
        yield response.follow(next_link, callback=self.parse, errback=self.handle_error)

    def bookData(self, response):
        """
            Collects the required information of each book from the given page and
            returns the data back to the parse method.
        """
        name = response.css("div.col-sm-6.product_main h1::text").get() or response.xpath("//div[@class='product_main']/h1/text()").get() or "None"
        price = response.css("div.col-sm-6.product_main p.price_color::text").get() or response.xpath("//div[@class='product_main']/p/text()").get() or "None"
        date_today = date.today().isoformat()
        try:
            description = response.xpath("//article[@class='product_page']/p/text()").get()
            if not description:
                description_more = response.css("article.product_page p::text").getall()[-1]
                description = description_more[-1]
        except Exception as e:
            print("ERROR IN FINDING DESCRIPTION!")
            description = "None"
        try:
            tax_more = response.css("table.table.table-striped tr td::text").getall() or response.xpath("//table/tr/td/text()").getall()
            tax = tax_more[4]
        except Exception as e:
            print("ERROR IN FINDING TAX!")
            tax = "None"
        try:
            availability_more = response.css("table.table.table-striped tr td::text").getall() or response.xpath("//table/tr/td/text()").getall()
            availability = availability_more[5]
        except Exception as e:
            print("ERROR IN FINDING AVAILABILITY!")
            availability = "None"
        try:
            upc_more = response.css("table.table.table-striped tr td::text").getall() or response.xpath("//table/tr/td/text()").getall()
            upc = upc_more[0]
        except Exception as e:
            print("ERROR IN FINDING upc VALUE!")
            upc = "None"
        try:
            rating_more = response.xpath("//div[contains(@class, 'col-sm-6')]/p/@class").getall()
            rating = rating_more[2].split()[1]
            if not rating:
                rating_more = response.css("div.col-sm-6.product_main p::attr(class)")[2].get()
                rating = rating_more.split(' ')[1]
        except Exception as e:
            print("ERROR IN FINDING RATING!")
            rating = "None"

        yield {
            "name": name,
            "url": response.url or "None",
            "scrape_date": date_today,
            "description": description,
            "price": price,
            "tax": tax,
            "availability": availability,
            "upc": upc,
            "rating": rating,
        }

    def handle_error(self, failure):
        self.logger.error(f"REQUEST FAILED: {failure.request.url}")
