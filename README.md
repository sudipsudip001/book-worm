## bookworm

bookworm is a web-scraper made using `scrapy` python that's made to scrape this book scraping [website](https://books.toscrape.com/). Here's how the scraper works:
- it starts at the homepage and collects all the links of books and for each book, visits its URL
- for each URL visited, which is the detailed information of the book, it collects necessary information such as name, price, description, upc, etc and yields those values.
- then at the end it collects the next page link to navigate to the next page and repeats the whole process until all the webpages have been scraped!

More focus has been on making the program capable of error handling and continuing despite the problems or lack of data that might occur. Also, both select by CSS and XPath have been used so that if one fails the other might work. It makes sure that the program keeps running even when some of the values might go missing or they can't be fetched.

In order to try it for yourself, the easiest way is to install Docker in your computer and follow the steps given below:

1. Clone the repository from github:
    - `git clone https://github.com/sudipsudip001/book-worm.git`
    - `cd book-worm/`

1. Build the docker container:
    - `docker build -t scrapy-uv-app .`

1. Make sure you have a folder named **output** in your repository and then run the container:
    - `docker run --rm -v $(pwd)/output:/app/output scrapy-uv-app crawl bookworm`

Optionally, if you don't want to use docker, you can also use `uv` package manager to run the program:

1. Clone the repository from github:
    - `git clone https://github.com/sudipsudip001/book-worm.git`
    - `cd book-worm/`

1. Sync the environment packages:
    - `uv sync`

1. Activate the virtual environment and open VS CODE:
    - `source .venv/bin/activate`
    - `code .`

1. Go to **settings.py** that is within book_worm folder inside your repository and uncomment the "books.json", and comment out for "/app/output/books.json"

1. Finally run the program:
    - `scrapy crawl bookworm -o books.json`

Docker option is preferable. In case you want to speed up the scraping you can change the **DOWNLOAD_DELAY** value in settings.py to something like 0.5 or 0.2.