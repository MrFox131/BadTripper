from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from fuzzywuzzy import fuzz
from typing import Optional, Tuple, Union, Any
import httplib2
from bs4 import BeautifulSoup, SoupStrainer

from sites_db import popular_sites
from free_zones import tropical_zones

app = FastAPI()


class Connection:
    def __init__(self, socket: WebSocket, url: str):
        self.socket = socket
        self.url = url
        self.closed = False
        self.check()

    async def check(self):
        pass
        await self.socket.close()
        self.closed = True

    def send(self):
        pass


class SocketManager:
    def __init__(self):
        self.connections = []

    async def connect(self, websocket: WebSocket, url: str):
        await websocket.accept()
        await websocket.send_json({"hello": "world"})
        self.connections.append(Connection(websocket, url))
        for conn in self.connections:
            if conn.closed:
                self.connections.remove(conn)
                del conn


socket_manager = SocketManager()


@app.websocket("/{url}")
async def get_url(websocket: WebSocket, url: str):
    await socket_manager.connect(websocket, url)


# returns None if no match, returns matching name if full(bool is true) or partial(bool is false) match. Full match does
# NOT guarantee positive result
async def check_on_domain_name_be_alike(domain_name: str) -> Optional[tuple[Any, bool]]:
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
async def check_domain_zone(domain_name: str):
    return domain_name.split(".")[-1] in tropical_zones


# generates all links from current page
async def get_all_links_from_site_generator(domain_name: str):
    http = httplib2.Http()
    status, response = http.request(domain_name)

    set_of_links = set()
    for link in BeautifulSoup(response, parse_only=SoupStrainer('link')):
        if link.has_attr('href'):
            yield link['href']
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            yield link['href']
    for img in BeautifulSoup(response, parse_only=SoupStrainer('img')):
        if img.has_attr('src'):
            yield img['src']
