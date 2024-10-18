# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from itemadapter import ItemAdapter
import os
from urllib.parse import urlparse


class CustomFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # Use the filename provided in the item metadata
        filename = item.get("file_name")
        if filename:
            # Ensure the filename is safe (no invalid characters)
            filename = self.sanitize_filename(filename)
            # Use the original file extension from the URL
            file_extension = os.path.splitext(urlparse(request.url).path)[1]
            return f"{filename}{file_extension}"
        else:
            # Fallback to the default file naming if no filename is found
            return super().file_path(request, response, info, item=item)

    def sanitize_filename(self, filename):
        # Remove or replace characters that are not safe for filenames
        return "".join(
            c for c in filename if c.isalnum() or c in (" ", ".", "_")
        ).rstrip()
