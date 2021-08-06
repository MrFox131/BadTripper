from time import time
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import SSL_check
from typing import List
import re
import requests
import time


def get_all_links_from_site_generator(domain_name: str) -> List[str]:
    # http = httplib2.Http()
    status, response = requests.get(domain_name)

    set_of_links = set()
    for link in BeautifulSoup(response, parse_only=SoupStrainer('link'), features="html.parser"):
        if link.has_attr('href'):
            yield link['href']
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href'):
            yield link['href']
    for img in BeautifulSoup(response, parse_only=SoupStrainer('img'), features="html.parser"):
        if img.has_attr('src'):
            yield img['src']

def start(hostname):
    urls = get_all_links_from_site_generator(hostname)
    
    ssl = SSL_check.start(hostname)
    all = 0
    alien_urls = 0
    try:
        for i in urls:
            all+=1
            if i.startswith("/"):
                continue
            else:
                i = i.split('/')[2 if i.startswith("http") else 0]
            
            found_match = False
            for subdomain in ssl["SAN"]:
                subdomain = subdomain.replace("*",".*")

                if re.match(subdomain, i):
                    found_match = True
                    break
            if not found_match:
                alien_urls += 1
    except:
        return 100.0

    return alien_urls/all*100


