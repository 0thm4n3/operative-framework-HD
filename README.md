<img src="https://image.ibb.co/fuPpQd/logo_operative.png" width="450">

**operative framework HD** is the digital investigation framework, you can interact with websites, email address, company, people, ip address ... interact with basic/graphical view and export with XML, JSON

## How to Install

install
+ mongoDB
+ NPM
+ Python

#### Create mongoDB database 
```
$ mongo
$ use operative_framework
$ db.createUser({user: 'operative', pwd:'operative', roles: [ "readWrite", "dbAdmin" ]})
```
For security restart now mongoDB with --auth argument
