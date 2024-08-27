from os import getenv
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from product_scraper.spiders.amazon import AmazonSpider


def main():
    load_dotenv(".env")
    search = getenv("SEARCH")
    url_host_ending = getenv("URL_HOST_ENDING", "com")

    # Set up the Scrapy settings
    settings = get_project_settings()

    # Create a CrawlerProcess with the settings
    process = CrawlerProcess(settings)

    # Add the spider to the process
    process.crawl(AmazonSpider, **{"search": search, "url_ending": url_host_ending})

    # Start the crawling process
    process.start()


if __name__ == "__main__":
    main()
