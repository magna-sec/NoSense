import Utils.Database
from Utils.Web import simple_get

from termcolor import cprint
import requests
from re import findall
from random import choice as rchoice



class Login():
    def __init__(self, name:str, url:str, username:str="Admin", password:str="pfsense", attemptLogin:bool=True) -> None:
        """Initialises the object.

        Args:
          name (str): Targets name
          url (str): Targets url
          username (str): Targets webgui username
          password (str): Targets webgui password
        Returns:
          None
        """
        # Attacker
        self.atkerIp = ""
        self.atkerLong = ""
        self.atkerIphex = ""
        # Target
        self.target_name = name
        self.targetUrl = url
        self.targetIp = url.split("/")[2]
        self.targetFile = ""
        self.targetArg = ""
        # Session
        self.session = requests.session()
        self.session.verify = False
        self.userAgent = self.get_useragent()
        self.loggedIn = False
        self.timeOut = 15
        self.DEBUG = False
        # Creds
        self.username = username
        self.password = password
        # CSRF
        self.__regex = "sid:.*;var"
        self.csrf = ""

        

        self.__ips()

        if(attemptLogin):
            result = self.__login()
            if(result != "failed"):
                self.loggedIn = True


    def get_useragent(self) -> str:
        with open("Lists/agents.txt", 'r') as filehandle:
            lines = filehandle.readlines()
            agent = rchoice(lines).strip()

        return agent

    def __ips(self):
        """Alter/Retrieve attackers IP details

        Args:
            self: Self object
        Returns:
            None
        """    
        dbConn = Utils.Database()
        attacker = dbConn.get_attacker()

        self.atkerIp = attacker.ip
        self.atkerLong = attacker.iplong
        self.atkerIphex = attacker.iphex

    def __login(self) -> str:
        """Log into the pfsense's webgui.

        Args:
            self: Self object
        Returns:
            None
        """    
        try:
            self.csrf = simple_get(self, "/", "", 0)
            self.session.verify = False

            # Actual Log In
            login_url = self.targetUrl + "/"
            login_headers = {"User-Agent": self.userAgent,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": self.targetUrl,
                    "Referer": self.targetUrl + "/index.php",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-User": "?1",
                    "Te": "trailers"}
            login_data = {"__csrf_magic": self.csrf, "usernamefld": self.username, "passwordfld": self.password, "login": "Sign In"}
        
            r = self.session.post(login_url, headers=login_headers, data=login_data, timeout=(self.timeOut, self.timeOut))
            if("pfSense - Login" in r.text):
                cprint("Login Failed", "red", end="")
                cprint(": ", "white", end="")
                cprint(self.targetUrl, "blue")
                return "failed"
            else:
                cprint("Logged In Successfully", "green", end="")
                cprint(": ", "white", end="")
                cprint(f"{login_url}", "blue")
                return findall(self.__regex, r.text)[0][:-5]
        except Exception as e:
            if(self.DEBUG): print(f"[+] Login Exception: {e}") 
            cprint("Login Failed", "red", end="")
            cprint(": ", "white", end="")
            cprint(self.targetUrl, "blue", end="")
            cprint(" - ", "white", end="")
            cprint("Potential Timeout ( You could be temporarily blocked )", "red")
            return "failed"