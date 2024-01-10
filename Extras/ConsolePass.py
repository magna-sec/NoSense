from Utils.Web import simple_get, simple_post

from termcolor import cprint

def toggle_console_pass(target):
    """
    """
    simple_get(target, "/system_advanced_admin.php", "", 0)
    postData = {"webguiproto":"https",
            "ssl-certref":"64ba8c8b8849a",
            "webguiport":"",
            "max_procs":"2",
            "loginautocomplete":"yes",
            "althostnames":"",
            "enablesshd":"yes",
            "sshdkeyonly":"disabled",
            "sshport":"",
            "sshguard_threshold":"",
            "sshguard_blocktime":"",
            "sshguard_detection_time":"",
            "address0":"",
            "address_subnet0":"128",
            "serialspeed":"115200",
            "primaryconsole":"serial",
            "disableconsolemenu":"yes",
            "save":"Save"
        }
    try:
        simple_post(target, "/system_advanced_admin.php", postData, 0)
        cprint("Enabled Console Password!", "blue")

    except:
        cprint("Unable to Enable Console Password!", "red")
