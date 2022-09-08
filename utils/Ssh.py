import utils
import os

def toggleSSH(details):
    utils.simpleGET(details, "/", "", 0)
    utils.loginPOST(details)
    utils.cmdGET(details, "echo 'y' | /etc/rc.initial.toggle_sshd")

def addSSHKey(details):

    user = input("Username: ")
    # Sets home e.g. /home/bob or /root depending on user
    home = "/user/%s" % (user)
    if(user == "root"): home = "/root"

    utils.simpleGET(details, "/", "", 0)
    utils.loginPOST(details)
    

    # Create SSH keys
    utils.cmdGET(details, 'HOSTNAME=`hostname` ssh-keygen -t rsa -C "$HOSTNAME" -f "%s/.ssh/id_rsa" -P "" && cat %s/.ssh/id_rsa.pub' % (home,home))
    utils.cmdGET(details, "touch -r %s/.cshrc ~/.ssh" % (home))

    # Read private key
    utils.cmdGET(details, "cat %s/.ssh/id_rsa" % (home))

    # Create unique id_rsa names per user, e.g. id_rsa_bob
    filename = "id_rsa_%s" % (user)
    with open(filename, 'w') as f:
        f.write(details.cmdOutput + "\n")
    # Permissions for private key
    os.popen("chmod 600 %s" % (filename))

    # Create authorized keys so don't need password
    utils.cmdGET(details, "cp %s/.ssh/id_rsa.pub %s/.ssh/authorized_keys && chmod 600 %s/.ssh/authorized_keys" % (home,home,home))

    # Hide creation date
    utils.cmdGET(details, "touch -r %s/.cshrc %s/.ssh" % (home,home))
    utils.cmdGET(details, "touch -r %s/.cshrc %s/.ssh/id_rsa" % (home,home))
    utils.cmdGET(details, "touch -r %s/.cshrc %s/.ssh/id_rsa.pub" % (home,home))
    utils.cmdGET(details, "touch -r %s/.cshrc %s/.ssh/authorized_keys" % (home,home))

def cmdSSH(details, user, cmd):
    
    details.cmdOutput = os.system("ssh %s@%s -i id_rsa_%s '%s'" % (user,details.pfsenseIP,user,cmd))

def addUser(details):
    utils.cmdSSH(details, "root", "adduser")

