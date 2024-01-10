# Option 10: Full Web Backdoor
## Summary
- ***BREAK GLASS OPTION***
- Requires valid web credentials

To be used only when other options are getting burnt, this attack is obvious as the firewall is restarted. This could have unknown effects, whilst also alerting the BT to your presence. However, at great cost comes great sneakiness 

# Example:
```bash
-> 10
##### Leet Backdoor #####
This will create:
-Login that will accept any password with valid username
-Disable Auth messages in pfsense shell
-Web shell on root page
-Reverse shell on root page
-PHPSESSIDs put in .ids.php

This will require a restart of the firewall, is that ok?
(1) Yes
(2) No
-> 1
Logged In Successfully
Upload Complete!
Pfsense Rebooting.....
```

## Overall Features:
- `IP Locked`
- `Encoded Parameter`
- `Time Stamped`
- `Default Pages`
- `Null Logs`

### OPSEC:
- 17 HTTP requests that I haven't listed becasuse of below
- Wipes logs
- Restarts Pfsense

## Fancy Login:
The `auth.inc` has been altered to be `IP Locked` allowing for the correct IP to login with `admin` and any password they want. This allows for total and utter control of the Pfsense machine. This will be very hard for the blue teams to spot, hence to be used as a break glass.
