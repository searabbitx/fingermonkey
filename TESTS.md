# Tests

## ownCloud 9.1.0

#### Running a docker container

```bash
docker run --rm -it -p 8888:80 owncloud/server:9.1.0
```

#### Gathering assets and cloning the repository

```bash
wget -r -erobots=off http://localhost:8888/ -P /tmp/owncloud_assets

git clone https://github.com/owncloud/core /tmp/owncloud_repo
```

#### Running the tool

```
$ ./fingermonkey.py /tmp/owncloud_repo /tmp/owncloud_assets 
...     

----====    Results    ====----

[+] Done! found 472 tags with at least one matching file
Top 10 tags:
  - v9.1.0RC4 (177 files matched)
  - v9.1.0RC3 (177 files matched)
  - v9.1.0RC2 (177 files matched)
  - v9.1.0RC1 (177 files matched)
  - v9.1.0    (177 files matched)
  - v9.1.1RC1 (176 files matched)
  - v9.1.3    (175 files matched)
  - v9.1.3RC1 (175 files matched)
  - v9.1.2    (175 files matched)
  - v9.1.2RC2 (175 files matched)
```

## roundcube mail 1.5.3

#### Running a docker container

```bash
docker run -e ROUNDCUBEMAIL_DEFAULT_HOST=mail -e ROUNDCUBEMAIL_SMTP_SERVER=mail --rm -it -p 8888:80 roundcube/roundcubemail:1.5.3-apache
```
#### Gathering assets and cloning the repository

```bash
wget -r -erobots=off http://localhost:8888/ -P /tmp/roundcube_assets

git clone https://github.com/roundcube/roundcubemail /tmp/roundcube_repo
```

#### Running the tool

```
$ ./fingermonkey.py /tmp/roundcube_repo /tmp/roundcube_assets 
...     

----====    Results    ====----

[+] Done! found 46 tags with at least one matching file
Top 10 tags:
  - 1.5.3    (27 files matched)
  - 1.5.2    (27 files matched)
  - 1.5.1    (27 files matched)
  - 1.5.0    (27 files matched)
  - 1.5-rc   (27 files matched)
  - 1.5-beta (27 files matched)
  - 1.4.13   (20 files matched)
  - 1.4.12   (20 files matched)
  - 1.4.11   (20 files matched)
  - 1.4.10   (20 files matched)
```

## nextcloud 22.2.10

#### Running a docker container

```bash
docker run --rm -it -p 8888:80 nextcloud:22.2.10-apache
```

#### Gathering assets and cloning the repository

```bash
wget -r -erobots=off http://localhost:8888/ -P /tmp/nextcloud_assets

git clone https://github.com/nextcloud/server /tmp/nextcloud_repo
```

#### Running the tool

```
$ ./fingermonkey.py /tmp/nextcloud_repo /tmp/nextcloud_assets 
...

----====    Results    ====----

[+] Done! found 517 tags with at least one matching file
Top 10 tags:
  - v22.2.10    (22 files matched)
  - v22.2.10rc2 (22 files matched)
  - v22.2.10rc1 (22 files matched)
  - v22.2.9     (22 files matched)
  - v22.2.9rc1  (22 files matched)
  - v22.2.8     (22 files matched)
  - v22.2.8rc1  (22 files matched)
  - v22.2.7     (21 files matched)
  - v22.2.7rc1  (21 files matched)
  - v22.2.6     (21 files matched)
```