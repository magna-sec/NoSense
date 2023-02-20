# NoSense
Create persistance/backdoors on a Pfsense 2.6.0 device.

# Target
```bash
22/tcp open  ssh     OpenSSH 7.9 (protocol 2.0)
53/tcp open  domain  (generic dns response: NOTIMP)
| fingerprint-strings: 
|   DNSVersionBindReqTCP: 
|     version
|_    bind
80/tcp open  http    nginx
|_http-title: pfSense - Login
```
# Setup
```bash
.\NoSense.py
# or
python3 NoSense.py
# Enter requested information, this will save into the .settings file
```
# Features:
- `Random Agent`:
Everytime you load `NoSense` you will use a different `User-Agent` in your requests.
- `IP Locked`:
When the script is uploaded the IP you entered in the setup or `.settings` file will be changed to the decimal equivilant. This is then put into the uploaded file and used to vet visitors. 
This IP doesn't have to be ur Kali box, this could also be any other machine you have access to and the knowledge to pull off the attacks.
- `Encoded Parameter`:
The parameter in use is encoded with `base64` to obfuscate the request. Future revisions this could be changed to encryption. Execute the following to get the approriate string.
```bash
echo -n "<CMD>" | base64
```
- `Time Stamped`:
The time stamp on the files is altered so a file just uploaded appears to be created at a different more appropriate date.
- `Default Pages`:
The attack in mention now uses hijacked default pages of the site to provide either a webshell or a reverse shell. Meaning the Blue Teams cannot simply remove them without breaking the functionality of Pfsense.
- `Null Logs`:
This option will send a CMD through the web interface to remove all Web and Auth logs from pfsense. The option will also link the files to `/dev/null` (via another file for obfuscation) so that any future requests won't be saved. See `11 Remove Auth and Web Logs` for more information.