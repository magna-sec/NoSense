import os

proxy_files = ["/etc/proxychains4.conf", "/etc/proxychains.conf"]
socks = []
chosen = ""
process = ""

def findProxy():
    global process

    try:
        process = os.popen("ps aux | grep 'ssh \-f \-N \-D'").read()
        process = process.split(" ")[7]
        return True
    except:
        print("No proxy found")
        return False
    


def getProxySettings():
    for fi in proxy_files:
        try:
            settings = fi
            f = open(settings, "r")
            for line in f:
                if("#" not in line):
                    if("socks" in line):
                        # socks4 127.0.0.1 9050
                        # to
                        # ['socks4', '\t127.0.0.1', '9050'] (this will get cleaned)
                        line = line.strip().split(" ")
                        socks.append(line[0] + "-" + line[2])
            break
        except:
            print("%s not found" % fi)

def chooseProxy():
    global chosen

    for p in socks:
        index = str(socks.index(p))
        print("Choose your proxy:")
        print("(" + index + ")" + ": " + p)

    choice = int(input("-> "))
    chosen = socks[choice]
    

def startProxy(details):
    global chosen
    port = chosen.split("-")[1]

    user = input("Username: ")

    # ssh -f -N -D 127.0.0.1:9050 root@192.168.190.190 -i 192_168_190_190/id_rsa_root
    os.system("ssh -f -N -D 127.0.0.1:%s %s@%s -i %s/id_rsa_%s" % (port,user,details.pfsenseIP,details.pfippath,user))

    print("Proxy Started!")

def stopProxy():
    global chosen

    os.system("sudo kill %s" % process)
    print("Proxy Killed!")

def toggleChains(details):
    if(findProxy()):
        print("Proxy found!")
        print("Do u wish to kill the process?")
        print("(1): Yes\n(2): No")
        choice = input("-> ")
        if(choice == "1"):
            stopProxy()
    else:
        print("Do u want to start a proxy?")
        print("(1): Yes\n(2): No")
        choice = input("-> ")
        if(choice == "1"):
            getProxySettings()
            chooseProxy()
            startProxy(details)
