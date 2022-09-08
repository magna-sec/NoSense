def loginPOST(details):
    # Actual Log In
    login_url = details.url + "/"
    login_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
             "Accept-Encoding": "gzip, deflate",
             "Content-Type": "application/x-www-form-urlencoded",
             "Origin": details.url,
             "Referer": details.url + "/index.php",
             "Upgrade-Insecure-Requests": "1",
             "Sec-Fetch-Dest": "document",
             "Sec-Fetch-Mode": "navigate",
             "Sec-Fetch-Site": "same-origin",
             "Sec-Fetch-User": "?1",
             "Te": "trailers"}
    login_data = {"__csrf_magic": details.csrf, "usernamefld": details.username, "passwordfld": details.password, "login": "Sign In"}
    r = details.session.post(login_url, headers=login_headers, data=login_data)

    if("pfSense - Login" in r.text): print("Login Failed"); loggedIn = False
    else: print("Logged In Successfully")
