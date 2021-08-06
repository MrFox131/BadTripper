import user_agent
import requests
def check_forwarding(url):
    check = True
    for i in range(3):
        r = requests.get(url,headers ={ 'User-Agent' : user_agent.get_user_agent()},allow_redirects=False)
        if "Location" in r.headers:
            url = r.headers["Location"]
            continue
        else:
            check  = False
            break
    return check
