#!/bin/bash

ssh root@138.68.1.36 "su postgres ; cd ; rm django3.bak ; pg_dump django3 > django3.bak ; exit ; exit"
scp root@138.68.1.36:/var/lib/postgresql/django3.bak ./django3.bak
