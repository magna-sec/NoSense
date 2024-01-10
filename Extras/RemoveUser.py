from Utils.Ssh import cmd_ssh

from termcolor import cprint
from re import findall

def remove_user(target, menuObject):
    """
    """
    found = 0
    # Define the regex pattern to match "pty/0" values
    pattern = r"pts\/\d"

    cmd = "who | grep 'pts'"
    try:
        output = cmd_ssh(target, "root", cmd)
    except:
        cprint("No Root Keys!", "red")
        return

    if("pts" in str(output)):
        cprint("USER FOUND", "red")
        found = 1
    else:
        cprint("No Users Logged in", "green")

    if(found):
        choice = menuObject.confirm_choice("Remove User?")

        if(choice):
            matches = findall(pattern, output)
            for m in matches:
                cmd = f"pkill -9 -t {m}"
                output = cmd_ssh(target, "root", cmd)



