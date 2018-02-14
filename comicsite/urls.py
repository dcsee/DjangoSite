from django.conf.urls import url
from . import views

urlpatterns = [
    
    #standard api for normal use
    url(r'^$', views.newest_post, name='newest_post'),
    url(r'^posts/id/(?P<post_id>[0-9]+)/$', views.permalink_post_by_id, name='permalink_post_by_id'),
#    url(r'^contact/$', views.contact, name='contact'),
    
    #xml api for ajax calls
    url(r'^xmlapi/search/(?P<search_text>.*)$', views.xml_search, name='xml_search'),
    url(r'^xmlapi/posts/$', views.xml_all_posts, name='xml_all_posts'),
    url(r'^xmlapi/posts/id/(?P<post_id>[0-9]+)/$', views.xml_post_by_id, name='xml_post_by_id'),
    url(r'^xmlapi/posts/tagged/(?P<tag>[\w|\-]+)/$', views.xml_posts_tagged, name='xml_posts_tagged'),
    url(r'^xmlapi/posts/categorized/(?P<category>[\S]+)/$', views.xml_posts_categorized, name='xml_posts_categorized'),
#    url(r'^xmlapi/contact/submit/$', views.xml_contact_submit, name='xml_contact_submit'),

    #social callback url
    url(r'^callback/social$', views.callback_social, name='callback_social')
]
