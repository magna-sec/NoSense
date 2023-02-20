# NoSense
Create multiple backdoors for Pfsense
# Web Shells
- Skidy:
  - Easily found 
  - Takes GET parameter cmd
- Amatuer:
  - Only accessible through host that uploaded it, otherwise an "error" is shown
  - Takes GET parameter c that is based64 encoded
- Pro:
  - Only accessible through host that uploaded it, otherwise the user is redirected
  - Takes POST parameter settings that is base64 encoded

# Reverse Shells
- Skidy:
  - Easily found
  - Takes GET parameters ip and Port
- Amatuer:
  - Only accessible through host that uploaded it, otherwise an "error" is shown
  - Takes GET parameter host that is base64 encoded
- Pro:
  - Only accessible through host that uploaded it, otherwise the user is redirected
  - Takes POST paramater route that is base64 encoded

# Backend Backdoors
- Create user
- Create SSH keys for specified user
- Open all WAN ports

# Full Backdoor
- Full Leet Backdoor:
  - Replaces auth.inc
    -  Allow admin with any password that comes from the uploaded host
    -  Hides logins etc in PFSense backend shell
  - Web Shell on root page
  - Reverse shell on root page
  - PHPSESSIDs dumped to .ids.php **Later to be used to steal sessions**
 
# To Fix/Make
- CronJobs
- Testing PHPSESSIDs
- Random shell names
- Encrypt Pro payloads
