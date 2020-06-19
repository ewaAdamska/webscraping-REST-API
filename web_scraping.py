import os
import requests
import re
from bs4 import BeautifulSoup


def get_soup_from_url(url):
    request = requests.get(url)
    html = request.content
    return BeautifulSoup(html, 'html.parser')

def scrap_text(site_url):  # TODO: maybe i should try to generate soup from page only once per each webstie scraping
    soup = get_soup_from_url(site_url)
    text = soup.get_text()  # depending on what exactly is needed we can easily change page text reading/formatting
    return re.sub(r'\n+', '\n', text)

# return dummy data just for now
def scrap_images(site_url):
    soup = get_soup_from_url(site_url)
    image_tags = soup.find_all('img')
    srcs = [img['src'] for img in image_tags]
    for src in srcs:
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png|svg))$', src)  # TODO: think about it,
        if not filename:
            print("Regex didn't match with the url: {}".format(src))
            continue

        with open(os.path.join('Images', filename.group(1)), 'wb') as f:
            if 'http' not in src:
                # sometimes an image source can be relative
                # if it is provide the base url which also happens
                # to be the site variable atm.
                src = f'{site_url}{src}'
            print(f'Img src {src}')
            response = requests.get(src)
            f.write(response.content)
    return []  # TODO: implement list of dicts with pictures properties

if __name__ == '__main__':
    # print(scrap_text("https://en.wikipedia.org/wiki/Web_scraping"))
    print(scrap_images("https://en.wikipedia.org/wiki/Web_scraping"))