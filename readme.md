# README

## Overview

This project is a web scraping tool designed to collect legal document metadata and associated PDFs from the website `https://congbobanan.toaan.gov.vn/`. The project consists of three main components: the crawler for scraping data, the PDF downloader, and a Jupyter notebook for data analysis.

### Running the Spider

To start the spider and crawl the legal documents, use the following command:

```
scrapy runspider banan.py
```

This will initiate a crawl of the website and save the metadata of the documents into the `output/banan.jsonl` file.

### Downloading PDFs

Once all links have been crawled, use the following command to download the associated PDFs:

```
scrapy runspider pdf.py
```

This will download the PDF files into the `output/pdf_files` directory, based on the metadata collected in the previous step.

### Data Analysis

The `analyze.ipynb` notebook is provided for analyzing the collected data. You can open and run it using Jupyter Notebook. This notebook uses `pandas` to load, clean, and analyze the metadata collected during the scraping process. You can also filter specific types of cases, such as criminal cases (`Hình sự`), and generate relevant insights.

### Requirements

- Python 3.6+
- Scrapy
- Jupyter Notebook
- Pandas

To install the necessary dependencies, you can use:

```
pip install scrapy pandas jupyter
```

### Project Structure

- `banan.py`: Scrapy spider for scraping metadata of legal documents.
- `pdf.py`: Scrapy spider for downloading PDFs of the collected documents.
- `analyze.ipynb`: Jupyter notebook for analyzing the scraped data.
- `output/`: Directory containing the scraped JSON lines file and downloaded PDFs.

### Notes

- Make sure to run `banan.py` before `pdf.py`, as the latter depends on the metadata collected by the former.
- The scraping process might take some time due to the large number of documents being crawled.

Feel free to reach out if you have any questions or need assistance!
