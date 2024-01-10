#!/usr/bin/python3
import Utils.Splash
import Utils.Database
import Utils.Menu

from termcolor import cprint

## Literally here to hide traceback on CTRL+C
from signal import signal, SIGINT
signal(SIGINT, lambda x,y: exit())

# Here to supress HTTPS warnings
from urllib3 import disable_warnings, exceptions
disable_warnings(exceptions.InsecureRequestWarning)

## Lets Go!
if __name__ == "__main__":
    amntFirewalls = ""
    Utils.Splash.display_splash()
    dbConn = Utils.Database()
    
    # Checks if database exists, if it does not, then make it.
    if not(dbConn.check_db()):
        while not(amntFirewalls.isnumeric()):
            cprint("Amount of firewalls: ", "blue", end="")
            amntFirewalls = input()
        amntFirewalls = int(amntFirewalls)
        dbConn.fill_db(amntFirewalls)
        Utils.Splash.display_splash()

    start_menu = Utils.Menu()