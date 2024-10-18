import scrapy
import csv
import os


class CsvFileDownloadSpider(scrapy.Spider):
    name = "csv_file_downloader"

    # Change these settings as needed
    CSV_FILE = "hinhsu_urls.csv"  # Path to the CSV file with URLs and names
    DOWNLOAD_DIRECTORY = (
        "output/pdf"  # Directory where files will be saved (updated to "output/pdf")
    )

    custom_settings = {
        "CONCURRENT_REQUESTS": 32,  # Increase the number of concurrent requests
        "RETRY_TIMES": 3,  # Set retry times for failed requests
        "DOWNLOAD_TIMEOUT": 15,  # Set a timeout for downloads to avoid getting stuck
        "CONCURRENT_REQUESTS_PER_DOMAIN": 32,  # More concurrent requests per domain
        "CONCURRENT_REQUESTS_PER_IP": 32,  # More concurrent requests per IP
        "AUTOTHROTTLE_ENABLED": False,  # Disable AutoThrottle
        "DOWNLOAD_DELAY": 0,  # Remove download delay
        "RANDOMIZE_DOWNLOAD_DELAY": False,  # Do not randomize download delay
        # "LOG_LEVEL": "INFO",  # Reduce log level to INFO for better performance
    }

    def start_requests(self):
        # Load URLs and filenames from the CSV file
        if not os.path.exists(self.CSV_FILE):
            self.log(
                f"CSV file {self.CSV_FILE} does not exist. Please provide a valid path."
            )
            return

        with open(self.CSV_FILE, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) < 2:
                    self.log(f"Invalid line in CSV: {row}")
                    continue

                file_url, filename = row
                yield scrapy.Request(
                    url=file_url, callback=self.save_file, meta={"filename": filename}
                )

    def save_file(self, response):
        # Ensure the directory exists
        if not os.path.exists(self.DOWNLOAD_DIRECTORY):
            os.makedirs(self.DOWNLOAD_DIRECTORY)

        # Get the filename from metadata passed in the request
        filename = response.meta["filename"]
        file_path = os.path.join(self.DOWNLOAD_DIRECTORY, filename)

        # Write the file to disk
        self.log(f"Saving file {filename} to {file_path}")
        with open(file_path, "wb") as f:
            f.write(response.body)


# To run this spider, save it to a Python file (e.g., `csv_file_download_spider.py`),
# and then execute it using Scrapy's command line interface like
