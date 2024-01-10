# Option 9: Execute a CMD via Web
## Summary

Execute a command through the web interface, this will by default run as `root`. This will require valid credentials for the web interface.

## Example
```bash
-> 9
Logged In Successfully
CMD: id
uid=0(root) gid=0(wheel) groups=0(wheel)
```

### OPSEC:
5 requests sent:
- GET request to root `/` to obtain phpsessid and __csrf_magic
- POST request to root `/` to log in
- GET request to root `/` following a 302 redirect from previous to dashboard
- GET request to `diag_command.php` to obtain csrfMagicToken
- POST request to `diag_command.php` to execute the command.