from django.http import HttpResponse
from django.core import exceptions
from .models import Blogpost

import datetime
import time
import sys
import re
import os


#controller methods (public interface)

def create_renderable_posts(posts):
    return [create_renderable_post(post) for post in posts]

def create_renderable_post(post):
    social_uris = {}

    if(post.twitter_uri):
        social_uris['twitter'] = post.twitter_uri

    if(post.tumblr_uri):
        social_uris['tumblr'] = post.tumblr_uri

    if(post.deviantart_uri):
        social_uris['deviantart'] = post.deviantart_uri

    post_to_post = {
        "title" : post.get_rendered_title(),
        "subtitle" : post.get_rendered_subtitle(),
        "hover_text" : post.hover_text,
        "description" : post.get_rendered_description(),
        "category" : post.category,
        "tags" : post.tags,
        "image_path" : post.image_path,
        "thumbnail_path" : post.thumbnail_path,
        "published_date" : post.published_date,
        "author" : post.author,
        "social_uris" : social_uris,
        "pk" : post.pk
    }
    return post_to_post


def find_search_results(search_text):
    results = set()
    lower_text = search_text.lower()
    terms = re.split(";|,| ", search_text)
    terms.append(search_text)
    terms = terms + re.split(";|,| ", lower_text)
    terms.append(lower_text)
    all_posts = Blogpost.objects.all().order_by('-published_date')

    for term in terms:
        results.update(_find_posts_with_tag(all_posts, term))
        results.update(_find_posts_in_category(all_posts, term))
        results.update(_find_posts_with_term_in_desc(all_posts, term))
    
    return results


def find_posts_categorized(category):
    formatted_category = category.replace("_"," ")
    all_posts = Blogpost.objects.all().order_by('-published_date')
    posts_categorized = _find_posts_in_category(all_posts, formatted_category)
    return posts_categorized

def find_posts_tagged(tag):
    formatted_tag = tag.replace("_"," ")
    all_posts = Blogpost.objects.all().order_by('-published_date')
    posts_tagged = _find_posts_with_tag(all_posts, formatted_tag)
    return posts_tagged

def posts_with_id(request, post_id):
    latest_post = Blogpost.objects.latest('published_date')
    return render(request, 'blog/single_post.html', {'latest_post' : latest_post})

def find_adjacent_post_ids(post):
    adjacent_post_ids = []
    try:
        #only show the 'first' and 'previous' link if not already on the first post
        first = Blogpost.objects.earliest('published_date')    
        if(post.pk > first.pk):
            adjacent_post_ids.append(('first', first.pk))
            all_previous = (Blogpost.objects.filter(published_date__lt=post.published_date)
                                            .order_by('-published_date'))
            if(all_previous.exists()):
                adjacent_post_ids.append(('previous', all_previous[0].pk))
    except exceptions.ObjectDoesNotExist:
        pass #I should really add logging here at some point  

    try:
        newest = Blogpost.objects.latest('published_date')
        if(post.pk < newest.pk):
            all_subsequent = (Blogpost.objects.filter(published_date__gt=post.published_date)
                                                .order_by('published_date'))
            
            if(all_subsequent.exists()):
                adjacent_post_ids.append(('next', all_subsequent[0].pk))
            #endif 
            adjacent_post_ids.append(('newest', newest.pk))
    except exceptions.ObjectDoesNotExist:
        pass
    return adjacent_post_ids 




def log_to_file(message, filename):
    full_message = "\n" + get_formatted_timestamp() + get_formatted_uid() + message
    print(full_message)
    logfile = open(filename, "a")
    logfile.write(full_message)
    logfile.close()


def post_not_found(post_id):
    message = ""

    if(post_id == -1):
        message = "Error 404 - post not found!"
    else:
        message = "Error 404 - post " + str(post_id) + " not found!"

    response = HttpResponse(message)
    response.status_code = 404
    return response

def get_formatted_uid():
    return " UID: " + str(os.getuid()) + " "

def get_formatted_timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

#utility methods (these should NOT be called from outside this file)

def _find_posts_with_tag(all_posts, tag):
    all_posts_with_tag = (
        filter(lambda current_post: current_post.contains_tag(tag), all_posts))
    return all_posts_with_tag


def _find_posts_in_category(all_posts, category):
    all_posts_in_category = (
        filter(lambda current_post: current_post.in_category(category), all_posts))
    return all_posts_in_category

def _find_posts_with_term_in_desc(all_posts, term):
    all_posts_containing_term = (
        filter(lambda current_post: current_post.desc_contains_term(term), all_posts))
    return all_posts_containing_term

