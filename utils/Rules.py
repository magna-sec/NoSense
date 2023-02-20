import utils

def enableAllWan(details):
    # Enables all ports open on WAN port
    command = "pfSsh.php playback enableallowallwan"

    # Send command
    utils.cmdSSH(details, "root", command)

