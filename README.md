# Amazon Product Scraper

This project is a Scrapy-based web scraper designed to extract product information from Amazon. It allows you to search for products based on a given query and supports scraping various product details.

## Environment Variables

The scraper requires two environment variables:

- **SEARCH** (mandatory): This is what the scraper will search.

- **URL_HOST_ENDING** (optional): This represents which country will be scraped. Defaults to 'com' (US Amazon).

## Output

The output data is stored in `data/amazon.json`.

## RUN

Run ```python3 main.py```