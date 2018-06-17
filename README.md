# operative framework HD
Operative a framework for investigator.

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



