from bs4 import BeautifulSoup
import requests
from Utils import utils


def get_description(domain):
    try:
        r = requests.get("http://" + domain)
    except requests.exceptions.RequestException as e:
        utils.log(e)
        return "No description"
    soup = BeautifulSoup(r.content, "html.parser")

    meta = soup.find_all('meta')
    for tag in meta:
        if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() == 'description':
            return tag.attrs['content']
        elif 'property' in tag.attrs.keys() and tag.attrs['property'].strip().lower() == 'og:description':
            return tag.attrs['content']

    return "No description"


def get_image(domain):
    try:
        r = requests.get("http://" + domain)
    except requests.exceptions.RequestException as e:
        utils.log(e)
        return "https://png.icons8.com/ios/50/000000/unavailable-cloud.png"
    soup = BeautifulSoup(r.content, "html.parser")

    meta = soup.find_all('meta')
    for tag in meta:
        if 'property' in tag.attrs.keys() and tag.attrs['property'].strip().lower() == 'og:image':
            return tag.attrs['content']
        elif 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() == 'twitter:image':
            return tag.attrs['content']

    return "https://png.icons8.com/ios/50/000000/unavailable-cloud.png"
