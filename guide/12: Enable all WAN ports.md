# Option 12: Enable all WAN Ports
- Requires valid web credentials

## Summary
This option will as stated "enable all WAN Ports" so anything that is open is open from any side. This is especially handy for the Web GUI, this may only be accessible on the LAN side, opening it from the WAN side too will enable the use of pivots and other attacks.

## Example:
```bash
-> 12
Adding allow all rule...
Turning off block private networks (if on)...
Turning off block bogon networks (if on)...
Reloading the filter configuration...
```

This can also be enabled manually through the SSH shell.
```bash
pfSsh.php playback enableallowallwan
```

### OPSEC:
5 requests sent:
- GET request to root `/` to obtain phpsessid and __csrf_magic
- POST request to root `/` to log in
- GET request to root `/` following a 302 redirect from previous to dashboard
- GET request to `diag_command.php` to obtain csrfMagicToken
- POST request to `diag_command.php` to execute the command.