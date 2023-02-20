import utils
import os
import base64

def toggleSSH(details):
    utils.simpleGET(details, "/", "", 0)
    utils.loginPOST(details)
    utils.cmdGET(details, "echo 'y' | /etc/rc.initial.toggle_sshd")

def addSSHKey(details):
    rsa_path = details.pfippath + "/" + "id_rsa_root"
    if not (os.path.exists(rsa_path)):
            print("Root RSA is required, pulling!")
            user = "root"
    else:
        user = input("Username: ")

    rsa_path = details.pfippath + "/" + "id_rsa_" + user
    # Sets home e.g. /home/bob or /root depending on user
    home = "/home/%s" % (user)
    if(user == "root"): home = "/root"

    utils.simpleGET(details, "/", "", 0)
    utils.loginPOST(details)
    
    print(home)
    # Create SSH keys
    utils.cmdGET(details, "mkdir %s/.ssh" % (home))
    utils.cmdGET(details, 'HOSTNAME=`hostname` ssh-keygen -t rsa -C "$HOSTNAME" -f "%s/.ssh/id_rsa" -P "" && cat %s/.ssh/id_rsa.pub' % (home,home))
    utils.cmdGET(details, "touch -r %s/.cshrc %s/.ssh" % (home, home))

    # Read private key
    utils.cmdGET(details, "cat %s/.ssh/id_rsa" % (home))

    # Create unique id_rsa names per user, e.g. id_rsa_bob
    with open(rsa_path, 'w') as f:
        f.write(details.cmdOutput + "\n")
    # Permissions for private key
    os.popen("chmod 600 %s" % (rsa_path))

    # Create authorized keys so don't need password
    utils.cmdGET(details, "cp %s/.ssh/id_rsa.pub %s/.ssh/authorized_keys && chmod 600 %s/.ssh/authorized_keys" % (home,home,home))

    # Change ownership to the correct user
    if not(user == "root"):
        utils.cmdGET(details, "chown %s %s/.ssh" % (user, home))
        utils.cmdGET(details, "chown %s %s/.ssh/id_rsa" % (user, home))
        utils.cmdGET(details, "chown %s %s/.ssh/id_rsa.pub" % (user, home))
        utils.cmdGET(details, "chown %s %s/.ssh/authorized_keys" % (user, home))
    # Hide creation date
    utils.cmdGET(details, "touch -r %s/.cshrc %s/.ssh" % (home,home))
    utils.cmdGET(details, "touch -r %s/.cshrc %s/.ssh/id_rsa" % (home,home))
    utils.cmdGET(details, "touch -r %s/.cshrc %s/.ssh/id_rsa.pub" % (home,home))
    utils.cmdGET(details, "touch -r %s/.cshrc %s/.ssh/authorized_keys" % (home,home))

    # Make user admin
    if not(user == "root"):
        choice = input("Want wheel etc privileges?\n(1) Yes\n(2) No\n-> ")
        if(choice == "1"):
            utils.cmdGET(details, "pw groupmod wheel -m %s" % (user))
            utils.cmdGET(details, "pw groupmod operator -m %s" % (user))
            utils.cmdGET(details, "pw groupmod admins -m %s" % (user))
            utils.cmdGET(details, "pw groupmod all -m %s" % (user))

    # Removing alert from web portal "ssh keys created blah blah"
    postdata = details.csrf + "&closenotice=all"
    utils.simplePOST(details, "/index.php", "", 0, postdata)

def cmdSSH(details, user, cmd):
    path = details.pfippath + "/" + "id_rsa_" + user
    details.cmdOutput = os.system("ssh %s@%s -i %s '%s'" % (user,details.pfsenseIP,path,cmd))

def addUser(details):
    utils.cmdSSH(details, "root", "adduser")
    
def scpSSH(details, user, direction, filename, path):
    rsa_path = details.pfippath + "/" + "id_rsa_" + user
    # From host to pfsense
    # scp -i 192_168_190_190/id_rsa_root /home/magna/DCM/NoSense/bob root@192.168.190.190:/tmp/yano
    if(direction == "0"):
        print("scp -i %s %s %s@%s:%s" % (rsa_path,filename,user,details.pfsenseIP,path))
        details.cmdOutput = os.system("scp -i %s %s %s@%s:%s" % (rsa_path,filename,user,details.pfsenseIP,path))
    # From pfsense to host
    # scp -i 192_168_190_190/id_rsa_root root@192.168.190.190:/etc/passwd bob
    if(direction == "1"):
        details.cmdOutput = os.system("scp -i %s %s@%s:%s %s" % (rsa_path, user, details.pfsenseIP,path,filename))

