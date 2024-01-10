
# Option 1: Upload a WebShell

- Requires credentials to create
- Doesn't require credentials to execute commands once uploaded.

Splits down into:
## Skidy:
Uploads a webshell to `<URL>/shell.php`. This shell takes the GET parameter `cmd` which will return the executed result e.g.

Use option `2` at the menu and select `Skidy` to access

### OPSEC:
5 requests sent:
- GET request to root `/` to obtain phpsessid and __csrf_magic
- POST request to root `/` to log in
- GET request to root `/` following a 302 redirect from previous to dashboard
- GET request to `diag_command.php` to obtain csrfMagicToken
- POST request to `diag_command.php` to upload the actual shell 
---
## Amatuer:
Uploads a webshell to `<URL>/vpn_l2tp_admin.php`. This shell takes the GET parameter `c`, which will return the executed result.
The wrong IP will return:
```cmd
Error: No GraphQL instance found.
```

Use option `2` at the menu and select `Amatuer` to access

### OPSEC:
5 requests sent:
- GET request to root `/` to obtain phpsessid and __csrf_magic
- POST request to root `/` to log in
- GET request to root `/` following a 302 redirect from previous to dashboard
- GET request to `diag_command.php` to obtain csrfMagicToken
- POST request to `diag_command.php` to upload the actual shell 

Features:
- `IP Locked`
- `Encoded Parameter`

---
## Pro:
Uploads a webshell to `<URL>/system_firewall_manager.php`. This shell takes the POST parameter `settings`, which will return the executed result. 
The wrong IP will redirect to `firewall_rules.php`

Use option `2` at the menu and select `Pro` to access

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


Features:
- `IP Locked`
- `Encoded Parameter`
- `Time Stamped`