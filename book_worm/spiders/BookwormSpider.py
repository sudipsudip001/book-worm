import scrapy
from datetime import date
from ..items import BookWormItem

class BookwormSpider(scrapy.Spider):
    name = "bookworm"
    start_urls = [
        "https://books.toscrape.com/",
    ]

    def __init__(self):
        self.date_today = date.today().isoformat()

    def parse(self, response):
        try:
            book_list = response.css("li.col-xs-6.col-sm-4.col-md-3.col-lg-3") or response.xpath("//ol[@class='row']//li[contains(@class, 'col-xs-6')]")
            for book in book_list:
                url = book.css("a::attr(href)").get() or book.xpath("//div[@class='image_container']/a/@href").get()
                yield response.follow(url, callback=self.bookData, errback=self.handle_error)
        except Exception:
            self.logger.error(f"COULDN'T SCRAPE DATA DUE TO FAILURE IN LINK.")
        # handle pagination
        next_link = response.css("li.next a::attr(href)").get() or response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield response.follow(next_link, callback=self.parse)

    def bookData(self, response):
        """
            Collects the required information of each book from the given page and
            returns the data back to the parse method.
        """
        if response.status != 200:
            return
        
        def extract_first(selector1, selector2, default="None"):
            return selector1.get() or selector2.get() or default

        name = extract_first(response.css("div.col-sm-6.product_main h1::text"), response.xpath("//div[contains(@class, 'product_main')]/h1/text()"))
        price = extract_first(response.css("div.col-sm-6.product_main p.price_color::text"), response.xpath("//div[contains(@class, 'product_main')]/p/text()"))

        table_data = response.css("table.table-striped tr") or response.xpath("//table/tr")
        table_dict = {row.css('th::text').get(): row.css('td::text').get() for row in table_data}
        
        upc = table_dict.get("UPC", "None")
        tax = table_dict.get("Tax", "None")
        availability = table_dict.get("Availability", "None")

        description = extract_first(response.css("article.product_page > p::text"), response.xpath("//article[@class='product_page']/p/text()"))

        rating_more = extract_first(response.css("div.col-sm-6.product_main p.star-rating::attr(class)"), response.xpath("//div[contains(@class, 'col-sm-6')]/p[contains(@class, 'star-rating')]/@class"))
        if rating_more is not "None":
            rating = rating_more.split(' ')[-1]
        else:
            rating = "None"

        yield BookWormItem(
            name = name,
            url = response.url or "None",
            scrape_date = self.date_today,
            description = description,
            price = price,
            tax = tax,
            availability = availability,
            upc = upc,
            rating = rating,
        )

    def handle_error(self, failure):
        self.logger.error(f"REQUEST FAILED: {failure.request.url}")

