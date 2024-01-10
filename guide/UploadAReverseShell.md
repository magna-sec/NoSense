# Option 3: Upload a Reverse Shell

- Requires credentials to create
- Doesn't require credentials to execute commands once uploaded.

Splits down into:
## Skidy:
Uploads a reverse shell to `<URL>/RevShell.php`. This file takes GET parameters `ip` and `port` which will return a php reverse shell.

Use option 4 at the menu and select `Skidy`
### OPSEC:
5 requests sent:
- GET request to root `/` to obtain phpsessid and __csrf_magic
- POST request to root `/` to log in
- GET request to root `/` following a 302 redirect from previous to dashboard
- GET request to `diag_command.php` to obtain csrfMagicToken
- POST request to `diag_command.php` to upload the actual shell 

---
## Amatuer:
Uploads a reverse shell to `<URL>/interfaces_ipv6.php`. This file takes a GET parameter of `host`. This is a concatanation of IP and Port, this will return a php reverse shell.

Use option 4 at the menu and select `Amatuer`

Features:
- `IP Locked`
- `Encoded Parameter`
### OPSEC:
5 requests sent:
- GET request to root `/` to obtain phpsessid and __csrf_magic
- POST request to root `/` to log in
- GET request to root `/` following a 302 redirect from previous to dashboard
- GET request to `diag_command.php` to obtain csrfMagicToken
- POST request to `diag_command.php` to upload the actual shell 

---
## Pro:
Uploads a reverse shell to `<URL>/system_advanced_routes.php`. This file takes a POST parameter of `route`. This is a concatanation of IP and Port, this will return a php reverse shell.

Use option 4 at the menu and select `Pro`

Features:
- `IP Locked`
- `Encoded Parameter`
- `Time Stamped`
### OPSEC:
9 requests sent:
- GET request to root `/` to obtain phpsessid and __csrf_magic
- POST request to root `/` to log in
- GET request to root `/` following a 302 redirect from previous to dashboard
- GET request to `diag_command.php` to obtain csrfMagicToken
- POST request to `diag_command.php` to upload the encoded shell
- GET request to `diag_command.php` to obtain csrfMagicToken
- POST request to `diag_command.php` to decode the shell
- GET request to `diag_command.php` to obtain csrfMagicToken
- POST request to `diag_command.php` to change time stamp of the shell