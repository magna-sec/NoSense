# Option 11: Remove Auth And Web Logs
## Summary
- Requires valid web credentials

This option will send a CMD through the web interface to remove all Web and Auth logs from pfsense. The option will also link the files to `/dev/null` (via another file for obfuscation) so that any future requests won't be saved.

This is a great way to cover any tracks you may have made, this is achieved by alterating the following files:

- `/var/log/nginx.log`
- `/var/log/auth.log`
- `var/log/system.log`
- `/var/log/userlog`

### OPSEC:
5 requests sent:
- GET request to root `/` to obtain phpsessid and __csrf_magic
- POST request to root `/` to log in
- GET request to root `/` following a 302 redirect from previous to dashboard
- GET request to `diag_command.php` to obtain csrfMagicToken
- POST request to `diag_command.php` to execute the command.

**HOWEVER**, these requests are removed in pfsense logs because of this option!