#!/bin/bash

#extract the comic files and copy the thumbnails to the static images directories
cd /home/django/django_project/comicsite/mgmt_scripts
tar -xvf ./deploy.tar.gz >> ./deploy_log
