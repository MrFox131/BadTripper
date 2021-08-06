from bs4 import BeautifulSoup
import user_agent
import requests
import urllib
def speller(url):
    API_BASE = 'https://speller.yandex.net/services/spellservice.json/checkText'
    source_code = requests.get(url,headers={'User-Agent':user_agent.get_user_agent()}).text
    soup = BeautifulSoup(source_code)
    text = soup.text[:200]
    r = requests.post(API_BASE, data={"text": text}).json()
    if len(text.split()) == 0:
        return 0
    return len(r)/len(text.split()) * 100
