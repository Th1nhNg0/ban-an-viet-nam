import csv
import os
import aiohttp
import asyncio
import urllib3
from aiohttp import ClientSession
from tqdm import tqdm  # Import the correct tqdm for progress bar

urllib3.disable_warnings()


# Function to download a PDF file asynchronously
async def download_pdf(session, url, filename):
    try:
        # Check if file already exists
        if os.path.exists(filename):
            return  # Skip download if file already exists

        # Create the output directory if it doesn't exist
        output_dir = os.path.dirname(filename)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Asynchronous download
        async with session.get(url, ssl=False) as response:
            if response.status == 200:
                # Save the PDF to the output directory
                with open(filename, "wb") as f:
                    f.write(await response.read())
    except Exception as e:
        # Optionally log the error here
        pass


# Function to read URLs and filenames from the CSV file
def read_csv(file_path):
    urls_and_filenames = []
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            url = row[0]
            filename = os.path.join(
                "output/pdf", row[1]
            )  # Save PDFs to output/pdf directory
            urls_and_filenames.append((url, filename))
    return urls_and_filenames


# Function to download PDFs in parallel with asyncio
async def download_pdfs_in_parallel(csv_file_path):
    urls_and_filenames = read_csv(csv_file_path)

    async with ClientSession() as session:
        tasks = [
            download_pdf(session, url, filename) for url, filename in urls_and_filenames
        ]

        # Use tqdm with asyncio.as_completed() for progress tracking
        for task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            await task


# Example usage:
if __name__ == "__main__":
    csv_file_path = "hinhsu_urls.csv"
    asyncio.run(download_pdfs_in_parallel(csv_file_path))
