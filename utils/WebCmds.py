import re
import urllib.parse
from random import randint

regex = "sid:.*;var"
cmd_regex = "(?s)<pre>.*<\/pre>"


def cmdGET(details, cmd):
    cmd_url = details.url + "/diag_command.php"
    cmd_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Referer": details.url,
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Te": "trailers"}
    r = details.session.get(cmd_url, headers=cmd_headers)
    details.csrf = re.findall(regex, r.text)[0][:-5]
    cmdPOST(details, cmd)

def cmdPOST(details, cmd):
    cmd_encoded = urllib.parse.quote_plus(cmd)
    mp_boundary = str(randint(100000000000000000000000000000, 999999999999999999999999999999))

    cmd_url = details.url + "/diag_command.php"
    cmd_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "multipart/form-data; boundary=---------------------------" + mp_boundary,
            "Origin": details.url,
            "Referer": details.url + "/diag_command.php",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Te": "trailers"}
    cmd_data = "-----------------------------"  + mp_boundary +"\r\n"
    cmd_data += 'Content-Disposition: form-data; name=\"__csrf_magic\"\r\n\r\n'
    cmd_data += details.csrf + "\r\n"
    cmd_data += "-----------------------------" + mp_boundary + "\r\n"
    cmd_data += 'Content-Disposition: form-data; name=\"txtCommand\"\r\n\r\n'
    cmd_data += cmd + "\r\n"
    cmd_data += "-----------------------------" + mp_boundary + "\r\n"
    cmd_data += "Content-Disposition: form-data; name=\"txtRecallBuffer\"\r\n\r\n"
    cmd_data += cmd_encoded + "\r\n"
    cmd_data += "-----------------------------" + mp_boundary + "\r\n"
    cmd_data += "Content-Disposition: form-data; name=\"submit\"\r\n\r\n"
    cmd_data += "EXEC\r\n"
    cmd_data += "-----------------------------" + mp_boundary + "\r\n"
    cmd_data += "Content-Disposition: form-data; name=\"dlPath\"\r\n\r\n\r\n"
    cmd_data += "-----------------------------" + mp_boundary + "\r\n"
    cmd_data += "Content-Disposition: form-data; name=\"ulfile\"; filename=\"\"\r\n"
    cmd_data += "Content-Type: application/octet-stream\r\n\r\n\r\n"
    cmd_data += "-----------------------------" + mp_boundary + "\r\n"
    cmd_data += "Content-Disposition: form-data; name=\"txtPHPCommand\"\r\n\r\n\r\n"
    cmd_data += "-----------------------------" + mp_boundary + "--\r\n"
    r = details.session.post(cmd_url, headers=cmd_headers, data=cmd_data)

    parseCMDOutput(details, r.text)



def parseCMDOutput(details, responseText):
    details.cmdOutput = re.findall(cmd_regex, responseText)[0][5:-6]

    print(details.cmdOutput) 
