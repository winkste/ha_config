# Home Assistant Configuration

## Installation

### Appdaemon 4
`
configuration: tcp: 5050
`

### Mosquitto Broker
```
logins: []
customize:
  active: false
  folder: mosquitto
certfile: fullchain.pem
keyfile: privkey.pem
require_certificate: false
```
### Terminal and SSH
```authorized_keys: []
apks: []
password: PASSWORD
server:
  tcp_forwarding: false
```
### MariaDB:
```databases:
  - homeassistant
logins:
  - username: homeassistant
    password: PASSWORD
rights:
  - username: homeassistant
    database: homeassistant
```
### SAMBA share:
```workgroup: WORKGROUP
username: homeassistant
password: PASSWORD
interface: ''
allow_hosts:
  - 10.0.0.0/8
  - 172.16.0.0/12
  - 192.168.0.0/16
  - fe80::/10
veto_files:
  - ._*
  - .DS_Store
  - Thumbs.db
  - icon?
  - .Trashes
compatibility_mode: false
```

### SSH
```
ssh root@192.168.178.45
````

## Configuring HASSIO config
### HASSIO configuration commands
```
ha core check
ha core restart
exit
````

### SMB connection for file transfer on MAC OSx
Open Finder and select:
```
Goto->Connect to server
```
Enter the SMB address of HASSIO:
```
smb://192.168.178.45
```

### Appdaemon
Web page of appdaemon:
```
http://192.168.178.45:5050
```
Appdaemon update procedure of apps:
```
stop appdaemon
update source files
start updaemon
```
### InfluxDB

### File Editor
```
dirsfirst: false
enforce_basepath: true
git: true
ignore_pattern:
  - __pycache__
  - .cloud
  - .storage
  - deps
ssh_keys: []
```


### Zigbee Home Automation
Using the conbee stick to integrate zigbee devices. 

### HACKS
Installation and configuration according to video tutorials:
https://www.youtube.com/watch?v=D6ZlhE-Iv9E

### HACKS Integrations
- swipe card
- mini-graph-card

### Backup HA image on OSs (not working)
```
diskutil list
sudo dd if=/dev/disk3 of=HaSDBackup.dmg
diskutil unmountDisk /dev/disk3
sudo dd if=HaSDBackup.dmg of=/dev/disk3
```

### TODO
- GITHUB via File Editor or SSH:
https://blog.schembri.me/post/syncing-homeassistant-with-github/

- How to backup the zigbee configurations, entities not found so far?

- update to new RASPI4 with ext SDD

- integrate fronius inverter
  - https://www.home-assistant.io/integrations/fronius/
  - https://community.home-assistant.io/t/fronius-integration-connection-failed/401288/4
  - Bei neuen GEN24-Geräten ab der Softwareversion 1.14 ist die Solar-API-Schnittstelle standardmäßig nicht aktiviert und muss bei Bedarf (z.B. Einbindung eines Fronius Wattpilot) aktiviert werden. Die Einstellung dazu finden Sie auf der Benutzeroberfläche des Wechselrichters unter "Kommunikation" - "Solar API".

- appdaemon compile in VSCode showing issues
