# Option 7: Toggle Proxychains
## Summary
- Requires a valid RSA key .e.g `id_rsa_root` or any other user. (can be obtained through option `5`->`1`)

This option will create a `local "dynamic" application-level port forwarding`. Meaning you are able to use the pfsense machine as a proxy to others. 


## Example
Start Proxy:
```bash
-> 7
No proxy found
Do u want to start a proxy?
(1): Yes
(2): No
-> 1
Choose your proxy:
(0): socks4-9050
-> 0
Username: root
Proxy Started!
```
You can check its live via:
```bash
ps aux | grep "ssh \-f \-N \-D"
# Ouputs:
magna       3991  0.0  0.1  25572  3984 ?        Ss   09:07   0:00 ssh -f - N  -D 9050 root@192.168.190.190 -i 192_168_190_190/id_rsa_root
```


We can now proxy through the machine by use `proxychains[4]`:
```bash
proxychains4 nmap -sT -Pn -n -p 666 192.168.190.155
```

Proof that its coming from SSH connection

- 11.807344 ***192.168.190.190*** → 192.168.190.155 TCP 74 47685 → 666 [SYN] Seq=0 Win=65228 Len=0 MSS=1460 WS=128 SACK_PERM=1 TSval=2499118554 TSecr=0
- 11.807377 192.168.190.155 → ***192.168.190.190*** TCP 74 666 → 47685 [SYN, ACK] Seq=0 Ack=1 Win=65160 Len=0 MSS=1460 SACK_PERM=1 TSval=3247518553 TSecr=2499118554 WS=128

### OPSEC:
A SSH connection is established to the pfsense machine, this could leak an IP, however it is possible to chain proxychains together, though that is beyond the scope of this documentation. 

Using this coupled with the `impacket` tools is highly sneaky!
