from Utils.Ssh import cmd_ssh

from termcolor import cprint

def enable_all_wan(target):
    # Enables all ports open on WAN port
    try:
        command = "pfSsh.php playback enableallowallwan"

        # Send command
        cmd_ssh(target, "root", command)
        cprint("Success! Ports should be open!", "yellow")
    except:
        cprint("Something went horribly wrong", "red")

