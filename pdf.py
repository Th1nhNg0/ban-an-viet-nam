import scrapy
from scrapy.http import Request
import os
import json


class PdfDownloaderSpider(scrapy.Spider):
    name = "pdf_downloader"
    custom_settings = {
        "LOG_LEVEL": "INFO",
        "CONCURRENT_REQUESTS": 100,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 50,
        "COOKIES_ENABLED": False,
    }

    def __init__(
        self,
        pdf_folder="output/pdf_files",
        input_file="output/banan.jsonl",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.pdf_folder = pdf_folder
        self.input_file = input_file
        os.makedirs(self.pdf_folder, exist_ok=True)

    def start_requests(self):
        if not os.path.isfile(self.input_file):
            self.logger.error(f"Input file {self.input_file} does not exist.")
            return

        with open(self.input_file, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                try:
                    record = json.loads(line)
                    record_id = record.get("id")
                    pdf_url = record.get("url")

                    if record_id and pdf_url:
                        modified_pdf_url = pdf_url.replace("2ta", "5ta")
                        yield Request(
                            url=modified_pdf_url,
                            callback=self.download_pdf,
                            meta={"record_id": record_id},
                            priority=10,
                            dont_filter=True,
                        )
                    else:
                        self.logger.warning(
                            f"Missing 'id' or 'url' in record on line {line_number}."
                        )
                except json.JSONDecodeError as e:
                    self.logger.error(f"Error decoding JSON on line {line_number}: {e}")

    def download_pdf(self, response):
        record_id = response.meta.get("record_id")
        if not record_id:
            self.logger.error("Missing record ID in response meta.")
            return

        pdf_path = os.path.join(self.pdf_folder, f"{record_id}.pdf")
        try:
            with open(pdf_path, "wb") as f:
                f.write(response.body)
            self.logger.info(
                f"Successfully downloaded PDF for record ID {record_id} to {pdf_path}"
            )
        except OSError as e:
            self.logger.error(f"Failed to save PDF for record ID {record_id}: {e}")
