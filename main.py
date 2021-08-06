from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fuzzywuzzy import fuzz
from typing import Optional
import httplib2
from bs4 import BeautifulSoup, SoupStrainer

from sites_db import popular_sites
from free_zones import tropical_zones

app = FastAPI()

@app.get("/")
def get_url(url: str):
    return JSONResponse(
        status_code=200,
        content={
            "hello": url
        }
    )


# returns None if no match, returns matching name if full(bool is true) or partial(bool is false) match. Full match does
# NOT guarantee positive result
def check_on_domain_name_be_alike(domain_name: str) -> Optional[(str, bool)]:
    original_name_without_zone = '.'.join(domain_name.split(".")[:-1])
    for checking_name in popular_sites:
        name_without_domain_zone = '.'.join(checking_name.split(".")[:-1])
        print(name_without_domain_zone)
        if 70 >= fuzz.ratio(original_name_without_zone, name_without_domain_zone) > 100:
            return checking_name, False
        elif fuzz.ratio(original_name_without_zone, name_without_domain_zone) == 100:
            return checking_name, True
    return None


# returns true if domain is free by default
def check_domain_zone(domain_name: str):
    return domain_name.split(".")[-1] in tropical_zones


# generates all links from current page
def get_all_links_from_site_generator(domain_name: str):
    http = httplib2.Http()
    status, response = http.request(domain_name)

    set_of_links = set()
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            href_formatted = '/'.join(link['href'].split("/")[:3])
            if href_formatted not in set_of_links:
                set_of_links.add(href_formatted)
                yield link['href']

