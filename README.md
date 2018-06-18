<img src="https://image.ibb.co/fuPpQd/logo_operative.png" width="450">

**operative framework HD** is the digital investigation framework, you can interact with websites, email address, company, people, ip address ...

## How to Install
Requirements:

+ MongoDB
+ Npm
+ Python


Create operative framework database

```
$ use operative_framework
$ db.createUser({user: 'operative', pwd:'operative', roles: [ "readWrite", "dbAdmin" ]})
```

For security restart now mongoDB with --auth argument



