from urllib import parse
from random import randint
from re import findall

regex = "sid:.*;var"
cmd_regex = "(?s)<pre>.*<\/pre>"
cmd2_regex = "(?s)</script>.*Gateway            Flags"

def cmd_GET(loginSession, cmd:str, view_output:bool) -> str:
    """
    """
    cmd_url = loginSession.targetUrl + "/diag_command.php"
    cmd_headers = {"User-Agent": loginSession.userAgent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Referer": loginSession.targetUrl,
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Te": "trailers"}
    r = loginSession.session.get(cmd_url, headers=cmd_headers)
    loginSession.csrf = findall(regex, r.text)[0][:-5]
    output = cmd_POST(loginSession, cmd, view_output)

    return output


def cmd_POST(loginSession, cmd:str, view_output:bool) -> str:
    """
    """
    cmd_encoded = parse.quote_plus(cmd)
    mp_boundary = str(randint(100000000000000000000000000000, 999999999999999999999999999999))

    cmd_url = loginSession.targetUrl + "/diag_command.php"
    cmd_headers = {"User-Agent": loginSession.userAgent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "multipart/form-data; boundary=---------------------------" + mp_boundary,
            "Origin": loginSession.targetUrl,
            "Referer": loginSession.targetUrl + "/diag_command.php",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Te": "trailers"}
    cmd_data = "-----------------------------"  + mp_boundary +"\r\n"
    cmd_data += 'Content-Disposition: form-data; name=\"__csrf_magic\"\r\n\r\n'
    cmd_data += loginSession.csrf + "\r\n"
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
    r = loginSession.session.post(cmd_url, headers=cmd_headers, data=cmd_data)
    
    output = parse_CMD_output(r.text, view_output)
    return output

def parse_CMD_output(responseText:str, view_output:bool) -> str:
    """
    """
    cmdOutput = "" 
    
    try:
        if("<pre>" in responseText): 
            cmdOutput = findall(cmd_regex, responseText)[0][5:-6]
        else: 
            cmdOutput = findall(cmd2_regex, responseText)[0][9:-32]
    except:
        pass

    if(view_output):
        print(cmdOutput, end="") 
    return cmdOutput