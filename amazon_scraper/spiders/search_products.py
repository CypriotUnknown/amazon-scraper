import scrapy
from scrapy.http import HtmlResponse
import re
from typing import Any
from requests.models import PreparedRequest


class SearchProductsSpider(scrapy.Spider):
    name = "search-products"
    allowed_domains = ["www.amazon.de"]

    custom_settings = {
        "FEEDS": {"amazon.json": {"format": "json", "indent": 4, "overwrite": True}}
    }

    def __init__(self, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        url_ending = kwargs.get("url_ending")
        self.base_url = f"https://www.amazon.{url_ending}"

        req = PreparedRequest()
        params = {"k": kwargs.get("search")}
        req.prepare_url(f"https://www.amazon.{url_ending}/s", params)
        self.start_urls = [req.url]

    def parse(self, response: HtmlResponse):
        products = response.xpath("//div[@data-asin]")

        for product in products:
            asin = product.xpath("@data-asin").get()

            if asin is None or len(asin) == 0:
                yield None
                continue

            url = product.xpath(".//a/@href").get()
            url = self.base_url + url if url else None

            imageURL = product.xpath(".//a//img/@src").get()
            title = product.xpath(".//div[@data-cy='title-recipe']//span/text()").get()
            stars = product.xpath(
                ".//div[@data-cy='reviews-block']//span/@aria-label"
            ).get()

            stars = self.parse_rating_string(stars) if stars else None

            reviews_count = product.xpath(
                ".//div[@data-csa-c-content-id='alf-customer-ratings-count-component']/span/@aria-label"
            ).get()

            reviews_count = (
                self.parse_review_count_str(reviews_count) if reviews_count else None
            )

            price_string = product.xpath(
                ".//a/span[@class='a-price']/span[@class='a-offscreen']/text()"
            ).get()

            price_currency = product.xpath(
                ".//span[@class='a-price-symbol']/text()"
            ).get()

            price = None

            if price_currency is not None and price_string is not None:
                try:
                    price_string = price_string.replace(price_currency, "")
                    price = {
                        "amount": float(price_string.replace(",", ".")),
                        "currency": price_currency,
                    }
                except Exception as e:
                    print("PRICE STRINGS:", price_string, asin, e)

            yield {
                "asin": asin,
                "url": url,
                "imageURL": imageURL,
                "title": title,
                "stars": stars,
                "reviews_count": reviews_count,
                "price": price,
            }

    def parse_rating_string(self, rating_str: str):
        pattern = r"(\d+([.,]\d+)?)"
        match = re.search(pattern, rating_str)

        if match:
            return float(match.group(1).replace(",", "."))

    def parse_review_count_str(self, review_str: str):
        pattern = r"(\d{1,3}(?:,\d{3})*)"
        match = re.search(pattern, review_str)

        if match:
            # Get the matched number with or without commas
            number_str = match.group(1)
            # Remove commas if they exist and cast to integer
            return int(number_str.replace(",", ""))
