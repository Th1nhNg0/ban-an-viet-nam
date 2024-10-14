import scrapy
from scrapy.http import Request
import os
import json


class PdfDownloaderSpider(scrapy.Spider):
    name = "pdf_downloader"
    custom_settings = {
        "FEED_EXPORT_ENCODING": "utf-8",
        "LOG_LEVEL": "INFO",
        "CONCURRENT_REQUESTS": 64,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1000,
        "REDIRECT_ENABLED": False,
        "COOKIES_ENABLED": False,
        "ROBOTSTXT_OBEY": False,
    }

    def __init__(self, *args, **kwargs):
        super(PdfDownloaderSpider, self).__init__(*args, **kwargs)
        self.pdf_folder = "output/pdf_files"
        self.input_file = "output/banan.jsonl"
        if not os.path.exists(self.pdf_folder):
            os.makedirs(self.pdf_folder)

    def start_requests(self):
        if not os.path.exists(self.input_file):
            self.logger.error(f"Input file {self.input_file} does not exist.")
            return

        with open(self.input_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    record_id = record.get("id")
                    if record_id:
                        pdf_url = record["url"].replace("2ta", "5ta")
                        yield Request(
                            url=pdf_url,
                            callback=self.download_pdf,
                            meta={"record_id": record_id},
                            priority=10,
                            dont_filter=True,
                        )
                except json.JSONDecodeError as e:
                    self.logger.error(f"Error decoding JSON: {e}")

    def download_pdf(self, response):
        record_id = response.meta["record_id"]
        pdf_path = os.path.join(self.pdf_folder, f"{record_id}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(response.body)
        self.logger.info(f"Downloaded PDF for record ID {record_id} to {pdf_path}")
