import csv
import requests
import os
from concurrent.futures import ThreadPoolExecutor
import urllib3
from tqdm import tqdm  # Import tqdm for progress bar

urllib3.disable_warnings()


# Function to download a PDF file
def download_pdf(url, filename):
    try:
        # Check if file already exists
        if os.path.exists(filename):
            return  # Skip download if file already exists

        # Disable SSL certificate verification
        response = requests.get(url, stream=True, verify=False)
        if response.status_code == 200:
            # Create the output directory if it doesn't exist
            output_dir = os.path.dirname(filename)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Save the PDF to the output directory
            with open(filename, "wb") as f:
                f.write(response.content)
        # No print statements for silent operation
    except Exception as e:
        # You can optionally log errors here if needed
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


# Function to download PDFs in parallel with progress bar
def download_pdfs_in_parallel(csv_file_path):
    urls_and_filenames = read_csv(csv_file_path)

    # tqdm progress bar wrapper
    with ThreadPoolExecutor(max_workers=64) as executor:
        list(
            tqdm(
                executor.map(lambda x: download_pdf(x[0], x[1]), urls_and_filenames),
                total=len(urls_and_filenames),
            )
        )


# Example usage:
csv_file_path = "hinhsu_urls.csv"
download_pdfs_in_parallel(csv_file_path)
