#!/bin/bash

rm deploy.tar.gz
tar -cvf deploy.tar.gz ./to_deploy
scp deploy.tar.gz django@138.68.1.36:/home/django/django_project/comicsite/mgmt_scripts/deploy.tar.gz