from bs4 import BeautifulSoup
import requests


def get_description(domain):
    r = requests.get("http://"+domain)
    soup = BeautifulSoup(r.content, "html.parser")

    meta = soup.find_all('meta')
    for tag in meta:
        if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() == 'description':
            return tag.attrs['content']
        elif 'property' in tag.attrs.keys() and tag.attrs['property'].strip().lower() == 'og:description':
            return tag.attrs['content']


def get_image(domain):
    r = requests.get("http://"+domain)
    soup = BeautifulSoup(r.content, "html.parser")

    meta = soup.find_all('meta')
    for tag in meta:
        if 'property' in tag.attrs.keys() and tag.attrs['property'].strip().lower() == 'og:image':
            return tag.attrs['content']
        elif 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() == 'twitter:image':
            return tag.attrs['content']
