from termcolor import cprint
from ipaddress import ip_address as check_ip
from validators import url as check_url


# Checks that the user is giving a valid IP address
def get_ip(name:str) -> str:
    """
    """
    ip = ""

    while not(ip):
        cprint(f"Enter {name} IP: ", "yellow", end="")
        in_ip = input()
        try:
            check_ip(in_ip)
            ip = in_ip
        except:
            cprint("Incorrect Format! \nExpects X.X.X.X", "red")
    return ip


def get_url(name:str ) -> str:
    """
    """
    url = ""
    while not(check_url(url)):
        cprint(f"Enter {name} URL: ", "yellow", end="")
        url = input()
        if not(check_url(url)):
            cprint("Incorrect Format! \nExpects http[s]://<DOMAIN>", "red")
    return url


