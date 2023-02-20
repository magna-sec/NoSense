# Option 8: Execute a CMD via SSH
## Summary

Execute a command through SSH either with `root` or a created account. However, this does require an RSA key, due to programming restraints.

## Example
```bash
-> 8
Username: magna
CMD: id
uid=1001(magna) gid=1001(magna) groups=1001(magna)
```

### OPSEC:
A SSH session is created as as the chosen user to pfsense and the supplied command is executed.