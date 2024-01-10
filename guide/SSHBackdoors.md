# Option 5: SSH Backdoors
Splits down into:
## SSH Keys
This will automatically try and create a `root` ssh keypair if one is not present in your pfsense IP folder (This is a folder created with the ip of pfsense server .e.g <PWD>/192_168_190_190)

This requires valid credentials to the web interface.

Once you have a `root` private key it can be used to create ones for other users.
Doing this sometimes can disable SSH so use option `10` to re-enable it.

```bash
Pick Backdoor
(1) SSH Keys
(2) Add User
(10) Toggle SSH
-> 1
```

Features:
- `Time Stamped`

### OPSEC:
22 Requests are sent: 
Not explained due to the amount

## Add User
When you have a `root` private key you can create users on the pfsense backend. 

e.g.:
```bash
Pick Backdoor
(1) SSH Keys
(2) Add User
(10) Toggle SSH
-> 2
```
The follow the prompts to create a user.

### OPSEC:
A SSH session is created as `root` to pfsense and the `adduser` command is executed.
## Toggle SSH
Sometimes SSH can get turned off or it may be turned off, it is possible to toggle it via the web interface. This requires valid credentials to the web interface.

```bash
Pick Backdoor
(1) SSH Keys
(2) Add User
(10) Toggle SSH
-> 10
```

### OPSEC:
5 requests sent:
- GET request to root `/` to obtain phpsessid and __csrf_magic
- POST request to root `/` to log in
- GET request to root `/` following a 302 redirect from previous to dashboard
- GET request to `diag_command.php` to obtain csrfMagicToken
- POST request to `diag_command.php` to execute the command enabling SSH