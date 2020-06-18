import requests
from bs4 import BeautifulSoup
import re


def scrap_text(url):
    request = requests.get(url)
    html = request.content
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return re.sub(r'\n+', '\n', text)

# return dummy data just for now
def scrap_images(url):
    return [
        {
        "path": "path_value",
        "filename": "filename_value",
        "size": 1024
        },
        {
        "path": "path_value_2",
        "filename": "filename_value_2",
        "size": 2048
        }
    ]

if __name__ == '__main__':
    print(scrap_text("https://en.wikipedia.org/wiki/Web_scraping"))