from django.core.management.base import BaseCommand
from comicsite.models import Blogpost
from comicsite.controllers import log_to_file
import sys

import pytumblr
#https://github.com/geduldig/TwitterAPI
from TwitterAPI import TwitterAPI

#using email as my DA interface
from django.core.mail import send_mail
from django.core.mail import get_connection
from django.core.mail import EmailMessage


FILE_PATH = "/home/django/django_project/comicsite/static/img/comics/"
SOCIAL_LOG = "/home/django/django_project/comicsite/mgmt_scripts/deploy_log"
TUMBLR_BLOG_URI = "https://raaky-draws.tumblr.com/"
DA_EMAIL_ADDRESS = ""
HOMEPAGE = "https://raakydesigns.art"

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--tumblr',
            action='store_true',
            dest='tumblr',
            help='Post to tumblr',
        )
        parser.add_argument(
            '--twitter',
            action='store_true',
            dest='twitter',
            help='Post to twitter',
        )
        parser.add_argument(
            '--deviantart',
            action='store_true',
            dest='deviantart',
            help='Post to deviantart',
        )

    def handle(self, *args, **options):
#        print(options)
        if(options['tumblr'] == True):
            to_tumblr()
        
        if(options['twitter'] == True):
            to_twitter()

        if(options['deviantart'] == True):
            to_deviantart()


def to_deviantart():
    post = Blogpost.objects.filter(category__exact="Raaky's World").order_by('-published_date')[0]

    if(post.deviantart_uri):
        log_to_file(
            " Did not send email to DA - DA URI already exists! " + post.deviantart_uri,
            SOCIAL_LOG)
        return

    post_info = _fetch_post_info(post)
    description = post_info['description'] + "\n\n"
    description += "<b>Enjoy more of Raaky's World on my homepage, <a href=\"" + HOMEPAGE + "\">Raaky Designs Art</a></b>\n\n"
    description += "Find me around the internet: <a href=\"https://raaky-draws.tumblr.com/\">tumblr</a> "
    description += "| <a href=\"https://twitter.com/raaky_draws\">twitter</a> | <a href=\"www.instagram.com/raaky_draws\">Instagram</a>"

    message = EmailMessage(

        #the subject
        post_info['title'],

        #the body
        description + "\n\n" + _format_tags(post_info['tag_list']),

        #the 'from'
        'raaky@raakydesigns.art',

        #the 'to'
        [DA_EMAIL_ADDRESS],
        connection=get_connection()
    )
    message.attach_file(post_info['absolute_file_path'])
    message.send(fail_silently=False)
    print(message)


def to_twitter():
    post = Blogpost.objects.filter(category__exact="Raaky's World").order_by('-published_date')[0]

    if(post.twitter_uri):
        log_to_file(
            "Did not post to twitter - twitter URI already exists! " + post.twitter_uri,
            SOCIAL_LOG)
        return

	#my real keys would go here - removed for public sharing
    api= TwitterAPI(
        'no',
        'no',
        'redacted',
        'still no')

    post_info = _fetch_post_info(post)
    post_text = "Raaky's World has updated! Read on " + HOMEPAGE + " " + _format_tags(post_info['tag_list'])
    image = open(post_info['absolute_file_path'])

    r = api.request('statuses/update_with_media',
                {'status': post_text},
                {'media[]': image.read()})

    response_json = r.json()
    twitter_uri = response_json['entities']['urls'][1]['expanded_url']
    post.twitter_uri = twitter_uri
    post.save()
    print('SUCCESS' if r.status_code == 200 else 'FAILURE')
    

def to_tumblr():
    post = Blogpost.objects.filter(category__exact="Raaky's World").order_by('-published_date')[0]
    
    if(post.tumblr_uri):
        log_to_file(
            "Did not post to tumblr - tumblr URI alraedy exists! " + post.tumblr_uri,
            SOCIAL_LOG)
        return

    post_info = _fetch_post_info(post)

	#I removed these keys too
    client = pytumblr.TumblrRestClient(
        'redacted',
        'classified',
        'very classified',
        'private',
    )

    response = client.create_photo("raaky-draws", state="published", tags=post_info['tag_list'], 
        caption=post_info['description'], data=post_info['absolute_file_path'])

    tumblr_uri = TUMBLR_BLOG_URI + "post/" + str(response['id']) + "/"
    post.tumblr_uri = tumblr_uri
    post.save()

    print(response)


def _format_tags(tag_list):
    tag_string = ""
    
    for tag in tag_list:
        tag = tag.replace("'", "")
        tag = tag.replace(" ", "")
        tag_string = tag_string + " #" + tag

    return tag_string


def _fetch_post_info(post):
    tag_list = post.tags.split(", ")
    tag_list.append(post.category)
    post_info = {
        'title' : post.title,
        'tag_list' : tag_list,
        'description' :  post.description,
        'absolute_file_path' : FILE_PATH + post.image_path 
    }
    return post_info
