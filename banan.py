import scrapy
from scrapy.http import Request
import os


class CongbobananSpider(scrapy.Spider):
    name = "banan"
    custom_settings = {
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_FORMAT": "jsonlines",
        "FEED_URI": "output/banan.jsonl",
        "LOG_LEVEL": "INFO",
        "JOBDIR": "output/job_data",
        "CONCURRENT_REQUESTS": 64,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1000,
        "REDIRECT_ENABLED": False,
        "COOKIES_ENABLED": False,
        "ROBOTSTXT_OBEY": False,
    }

    def __init__(self, *args, **kwargs):
        super(CongbobananSpider, self).__init__(*args, **kwargs)
        self.pdf_folder = "output/pdf_files"
        if not os.path.exists(self.pdf_folder):
            os.makedirs(self.pdf_folder)

    start_urls = [
        f"https://congbobanan.toaan.gov.vn/2ta{i}t1cvn/" for i in range(1, 1700000)
    ]

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

    def download_pdf(self, response):
        record_id = response.meta["record_id"]
        pdf_path = os.path.join(self.pdf_folder, f"{record_id}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(response.body)
