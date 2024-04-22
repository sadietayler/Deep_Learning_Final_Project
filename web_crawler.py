import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# This script takes the file "temples.txt" as input. This text file contains urls for all the temples that are currently operating or under renovation. 

def download_images(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Only download images from the Gallery section
    gallery = soup.find('div', id='GalleryDiv')
    if gallery:
        images = gallery.find_all('img')
        for i, img in enumerate(images):
            img_url = img.get('src')
            if not img_url.startswith(('http:', 'https:')):
                img_url = urljoin(url, img_url)  # Handle relative URLs
            print(f"Downloading {img_url} into {folder}")
            img_data = requests.get(img_url).content
            with open(os.path.join(folder, f'image_{i}.jpg'), 'wb') as handler:
                handler.write(img_data)
    else:
        print(f"No 'Gallery' section found at {url}")


def main():
    with open('temples.txt', 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        temple_name = url.split('/')[-3]
        folder = f"downloaded_images/{temple_name.replace(' ', '_')}"
        print(f"Processing {temple_name}")
        download_images(url, folder)


if __name__ == "__main__":
    main()
