import os
import re
from datetime import datetime
from uuid import uuid4

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from headers import mj_headers


def fetch_image_urls(html_file_path):
    """
    Extracts image URLs from the specified HTML file.

    :param html_file_path: Path to the HTML file to parse.
    :return: A list of image URLs.
    """
    with open(html_file_path) as file:
        soup = BeautifulSoup(file, "html.parser")

    pattern = r"https:\/\/cdn\.midjourney\.com\/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\/[^ ]+\.webp"
    return re.findall(pattern, str(soup))


def download_images(image_urls, destination_folder):
    """
    Downloads images from the provided URLs into the specified folder.

    :param image_urls: List of image URLs to download.
    :param destination_folder: Folder path where images will be saved.
    """
    if not image_urls:
        print("No image URLs provided.")
        return

    os.makedirs(destination_folder, exist_ok=True)

    #! This is important to avoid getting blocked!
    headers = mj_headers

    for url in tqdm(image_urls):
        try:
            filename = os.path.join(destination_folder, f"{uuid4()}.webp")
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
            else:
                print(f"Failed to download {url} - Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"An error occurred while downloading {url}: {e}")


if __name__ == "__main__":
    html_file_path = "./Midjourney Feed.html"
    destination_folder = datetime.now().strftime("%Y%m%d")

    image_urls = fetch_image_urls(html_file_path)
    download_images(image_urls, destination_folder)
