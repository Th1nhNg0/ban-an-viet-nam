import scrapy
import csv
import os


class CsvFileDownloadSpider(scrapy.Spider):
    name = "csv_file_downloader"

    # Path to the CSV file with URLs and names
    CSV_FILE = "hinhsu_urls.csv"

    custom_settings = {
        "CONCURRENT_REQUESTS": 100,  # Adjust concurrency as needed
        "CONCURRENT_REQUESTS_PER_DOMAIN": 100,
        "RETRY_TIMES": 3,
        "DOWNLOAD_DELAY": 0,
        "LOG_LEVEL": "INFO",
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "COOKIES_ENABLED": False,
        "ITEM_PIPELINES": {
            "myproject.pipelines.CustomFilesPipeline": 1,
        },  # Referencing pipeline properly
        "FILES_STORE": "output/pdf",
        "FEED_FORMAT": "jsonlines",
        "FEED_URI": "output/pdf_files.jsonl",
    }
    start_urls = [
        "https://www.example.com",
    ]

    def parse(self, response):
        # Check if the CSV file exists
        if not os.path.exists(self.CSV_FILE):
            self.logger.error(
                f"CSV file {self.CSV_FILE} does not exist. Please provide a valid path."
            )
            return

        # Open and read the CSV file
        with open(self.CSV_FILE, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) < 2:
                    self.logger.warning(f"Invalid line in CSV: {row}")
                    continue

                file_url, filename = row
                filename = filename.strip()

                if filename:
                    yield {
                        "file_name": filename,
                        "file_urls": [file_url],
                    }
