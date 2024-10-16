import scrapy
from scrapy.http import Request
import os


class CongbobananSpider(scrapy.Spider):
    name = "banan"
    custom_settings = {
        # "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_FORMAT": "jsonlines",
        "FEED_URI": "output/banan.jsonl",
        "LOG_LEVEL": "INFO",
        "CONCURRENT_REQUESTS": 100,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 100,
        # disable cookie
        "COOKIES_ENABLED": False,
        # disable retry
        "RETRY_ENABLED": False,
    }

    # start_urls = [
    #     f"https://congbobanan.toaan.gov.vn/2ta{i}t1cvn/" for i in range(1, 1700000)
    # ]

    def start_requests(self):
        for i in range(1, 1700000):
            yield Request(
                url=f"https://congbobanan.toaan.gov.vn/2ta{i}t1cvn/",
                callback=self.parse,
                dont_filter=True,
            )

    def parse(self, response):
        title = response.css("title::text").extract_first().strip()
        if title == "null" or not title or title == "":
            return

        table = response.css(
            "#aspnetForm > section > div > div > div > div.col-xs-12.col-sm-5.col-md-4.col-lg-4 > div.search_left_pub.details_pub > div > ul",
        )
        metadata = {}
        # for li in table: metadata title = <label> tag, value = <span> tag
        for li in table.css("li"):
            label = li.css("label::text").get()
            value = li.css("span::text").get()
            if label and value:
                metadata[label.strip()] = value.strip()

        record_id = response.url.split("/")[-2]

        date = response.css("#\\31 b > div.title_detai_tab_pub > span::text").get()
        yield {
            "id": record_id,
            "url": response.url,
            "date": date,
            **metadata,
        }
        # pdf_url = response.url.replace("2ta", "5ta")
        # yield Request(
        #     url=pdf_url,
        #     callback=self.download_pdf,
        #     meta={"record_id": record_id},
        #     priority=10,  # Higher priority for downloading PDFs
        #     dont_filter=True,
        # )
