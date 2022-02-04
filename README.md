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

### TODO
- GITHUB via File Editor or SSH:
https://blog.schembri.me/post/syncing-homeassistant-with-github/

- How to backup the zigbee configurations, entities not found so far?
