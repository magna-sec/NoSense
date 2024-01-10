# Option 6: SCP Files

## Summary
This uses SSH keys to upload and download files from the pfsense machine. 

Please use absolute paths:
- `/home/magna/test`

Not releative paths
- `../../magna/test` or `~/test`

Splits down into:

## Upload File
```bash
Upload File (0)
Download File (1)
-> 0
Username: magna          
File to upload: /home/magna/DCM/test
Path on pfsense to upload to: /tmp/test
```
### OPSEC
A SSH session is created as the selected user to pfsense and the file is copied.

## Download File
```bash
Upload File (0)
Download File (1)
-> 1
Username: magna
Full path of file to download: /tmp/test
Output file name: /home/magna/DCM/test
```
### OPSEC:
A SSH session is created as the selected user to pfsense and the file is copied.

