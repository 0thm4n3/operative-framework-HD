<img src="https://image.ibb.co/fuPpQd/logo_operative.png" width="450">

**operative framework HD** is the digital investigation framework, you can interact with websites, email address, company, people, ip address ... interact with basic/graphical view and export with XML, JSON

<img src="https://preview.ibb.co/jA9iqJ/Capture_d_e_cran_2018_06_18_a_20_28_34.png" width="450">

## How to Install

You need this packages
+ mongoDB
+ NPM
+ Python 2

#### Create mongoDB database 
```
$ mongo
$ use operative_framework
$ db.createUser({user: 'operative', pwd:'operative', roles: [ "readWrite", "dbAdmin" ]})
```
For security restart now mongoDB with --auth argument

#### install globally a operative framework HD
```
$ git clone https://github.com/graniet/operative-framework-HD.git
$ cd operative-framework-HD
$ chmod +x install.sh
$ ./install.sh
```

#### create first user
```
$ sudo opf_users
opf_users > create operative Op3r4tIv3P$$SS
```

#### run operative framework without console
first shell:
```
$ sudo opf_server
```
second shell:
```
$ sudo opf_client
```

#### run operative framework with console
```
$ sudo opf_console
$ opf_console > run_server
$ opf_console > run_client
```
