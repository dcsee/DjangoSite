from django.core.management.base import BaseCommand
from comicsite.controllers import log_to_file
from comicsite.models import Blogpost
from subprocess import call
import datetime
import time
import json
import os

MGMT_DIR = "/home/django/django_project/comicsite/mgmt_scripts"
COMIC_DATA_SRC_PATH = MGMT_DIR + "/to_deploy"
DEPLOY_LOG = MGMT_DIR + "/deploy_log"

COMIC_IMAGE_DEST_PATH = "/home/django/django_project/comicsite/static/img/comics/"
COMIC_THUMB_DEST_PATH = "/home/django/django_project/comicsite/static/img/thumbs/"

COMIC_DATA_NAME = "/comic_data.json"

class Command(BaseCommand):


    def handle(self, *args, **options):

        #read in the comic data. If no data, log and exit
        data_file_name = COMIC_DATA_SRC_PATH + COMIC_DATA_NAME

        if not os.path.isfile(data_file_name):
            log_to_file(
                " Comic deploy failed - data file " + data_file_name + " not found.", DEPLOY_LOG)
            return


        json_data=open(COMIC_DATA_SRC_PATH + COMIC_DATA_NAME).read()
        data = json.loads(json_data)

        #if the data is empty, log the error and quit
        if not data:
            log_to_file(
                " Comic deploy failed - failed to read data file.", DEPLOY_LOG)
            return

        #copy images to static directory
        os.rename(COMIC_DATA_SRC_PATH + "/" + data['image_path'], 
            COMIC_IMAGE_DEST_PATH + data['image_path'])
        os.rename(COMIC_DATA_SRC_PATH + "/" + data['thumbnail_path'], 
            COMIC_THUMB_DEST_PATH + data['thumbnail_path'])

        #create the post
        post = Blogpost.create()
        post.title = data['title']
        post.subtitle = data['subtitle']
        post.hover_text = data['hover_text']
        post.description = data['description']
        post.category = data['category']
        post.tags = data['tags']
        post.image_path = data['image_path']
        post.thumbnail_path = data['thumbnail_path']
        post.save()

        #cleans up the tarball and temp folder
        call([MGMT_DIR + "/cleanComic.sh"])

        log_to_file(" add_comic.py completed with no errors detected", DEPLOY_LOG)

