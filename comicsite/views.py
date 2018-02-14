from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
import sys

from .models import Blogpost
import controllers
import json


CALLBACK_LOG = "/home/django/django_project/comicsite/mgmt_scripts/callback_log/log"
PARENT_MASTER = 'comicsite/parent_master.html'
POSTS_SEARCHED = 'comicsite/posts_searched.html'
SINGLE_POST = 'comicsite/single_post.html'
CONTACT = 'comicsite/contact.html'

#permalink api
def permalink_post_by_id(request, post_id):
    try:
        post_original = Blogpost.objects.get(pk=post_id)
        post_renderable = controllers.create_renderable_post(post_original)
        return _render_with_include(request, post_renderable, post_original, 
            PARENT_MASTER, SINGLE_POST)
    except:
        return controllers.post_not_found(post_id)

def contact(request):
    return _render_include_no_post(request, PARENT_MASTER, CONTACT)



#xml api
def xml_search(request, search_text):
    return search(request, search_text, POSTS_SEARCHED)
def xml_all_posts(request):
    return all_posts(request, POSTS_SEARCHED)
def xml_post_by_id(request, post_id):
    return post_by_id(request, post_id, SINGLE_POST)
def xml_posts_tagged(request, tag):
    return posts_tagged(request, tag, POSTS_SEARCHED)
def xml_posts_categorized(request, category):
    return posts_categorized(request, category, POSTS_SEARCHED)

#def xml_contact_submit(request):
#    response = HttpResponse("Message received! " + 
#        str(request.GET) + str(request.POST) + str(request.method) + str(request.path))
#    response.status_code = 200
#    return response
#    payload = json.loads(request.body)
#    filename = "/django_project/comicsite/mgmt_scripts/contacts/"
#    filename += controllers.get_formatted_timestamp()
#    filename += " " + payload['name']
#    contact_submission = open(filename, "w+")
#    contact_submission.write(payload['name'] + "\n\n")
#    contact_submission.write(payload['email'] + "\n\n")
#    contact_submission.write(payload['message'] + "\n\n")
#    contact_submission.close()

#common api implementation
def search(request, search_text, template):
    results = controllers.find_search_results(search_text)
    return render(request, template, 
        {
            'posts_found' : controllers.create_renderable_posts(results),
            'status_message' : str(len(results)) + " results found:"
        })


def newest_post(request):
    post_original = Blogpost.objects.latest('published_date')
    post_renderable = controllers.create_renderable_post(post_original)
    return _render_with_include(request, post_renderable, post_original, 
        PARENT_MASTER, SINGLE_POST)

def all_posts(request, template):
    all_posts = Blogpost.objects.all().order_by('-published_date')
    return render(request, template, 
        {
            'posts_found' : controllers.create_renderable_posts(all_posts)
        })

def post_by_id(request, post_id, template):
    try:
        post_original = Blogpost.objects.get(pk=post_id)
        post_renderable = controllers.create_renderable_post(post_original)
        return _render_single_post(request, post_renderable, post_original, template)
    except:
        return controllers.post_not_found(post_id)

def posts_tagged(request, tag, template):
    posts_tagged = controllers.find_posts_tagged(tag)
    return render(request, template, 
        {
            'posts_found' : controllers.create_renderable_posts(posts_tagged)
        })

def posts_categorized(request, category, template):
    posts_categorized = controllers.find_posts_categorized(category)
    return render(request, template, 
        {
            'posts_found' : controllers.create_renderable_posts(posts_categorized)
        })







#utility methods - do not call outside this class!
def _render_with_include(request, post_renderable, post_original, 
    parent_template, include_template):
    return render(request, parent_template, 
        {
            'post' : post_renderable,
            'display_to_URL_tags' : post_original.get_tags_to_URL_tags(),
            'display_to_URL_category' : post_original.get_category_to_URL_category(),
            'adjacent_post_ids' : controllers.find_adjacent_post_ids(post_original),
            'include_template' : include_template
        })
def _render_single_post(request, post_renderable, post_original, template):
    return render(request, template, 
        {
            'post' : post_renderable,
            'display_to_URL_tags' : post_original.get_tags_to_URL_tags(),
            'display_to_URL_category' : post_original.get_category_to_URL_category(),
            'adjacent_post_ids' : controllers.find_adjacent_post_ids(post_original)
        })
def _render_include_no_post(request, parent_template, include_template):
    return render(request, parent_template, 
        {
            'include_template' : include_template
        })

#the social callback
def callback_social(request):
    controllers.log_to_file(request.method + " " + request.body, CALLBACK_LOG)
    response = HttpResponse("Callback received")
    response.status_code = 200
    return response
