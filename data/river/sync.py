import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, "files")

max_files_to_download = 1000 # to prevent github workflow timeout


def download_file(url, filename):
    print("Downloading:", filename)
    response = requests.get(url + filename)
    response.raise_for_status()

    with open(os.path.join(FILES_DIR, filename), "wb") as f:
        f.write(response.content)


def download_all(url, files, workers=25):
    os.makedirs(FILES_DIR, exist_ok=True)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(lambda f: download_file(url, f), files)


def sync_files(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    files = []

    for link in soup.find_all("a"):
        href = link.get("href")

        if (
            not href
            or href == "../"
            or os.path.exists(os.path.join(FILES_DIR, href))
            # downloading only pdf for now (majority and latest). there are odt, jpg, png, xlsx files too.
            or not href.lower().endswith("pdf")
        ):
            print("Skipping", href)
            continue
        files.append(href)

    print("Downloading", len(files), "files")
    if len(files) > max_files_to_download:
        print("Limiting to", max_files_to_download, "files")
        files = files[:max_files_to_download]
    download_all(url, files)


sync_files("https://www.dmc.gov.lk/images/dmcreports/")
