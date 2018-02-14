from django.db import models
from django.utils import timezone
import markdown

class Blogpost(models.Model):
    title = models.CharField(max_length=161, unique=True)
    subtitle = models.CharField(max_length=160, unique=False)
    hover_text = models.CharField(max_length=160, default="", unique=False, blank=True)
    description = models.TextField(unique=False)
    category = models.CharField(max_length=40, default="uncategorized", unique=False)
    tags = models.CharField(max_length=160, unique=False)
    image_path = models.CharField(max_length=160, default="", unique=True, blank=True)
    thumbnail_path = models.CharField(max_length=160, default="", unique=True, blank=True)
    published_date = models.DateTimeField(default=timezone.now, unique=True)

    #default author
    author = models.ForeignKey('auth.User', default=1)

    #social URLs
    tumblr_uri = models.CharField(max_length=254, default="", unique=False, blank=True)
    twitter_uri = models.CharField(max_length=254, default="", unique=False, blank=True)
    deviantart_uri = models.CharField(max_length=254, default="", unique=False, blank=True)



    @classmethod
    def create(cls):
        post = cls()
        # do something with the book
        return post

#all these 'get_rendered' methods return the indicated attribute, rendered from markdown to html

    def get_rendered_title(self):
        return markdown.markdown(self.title)

    def get_rendered_subtitle(self):
        return markdown.markdown(self.subtitle)

    def get_rendered_description(self):
        return markdown.markdown(self.description)

    def contains_tag(self, tag):
        tag_array = self._make_string_param_array(self.tags)
        return tag in tag_array

    def in_category(self, category):
        category_array = self._make_string_param_array(self.category)
        return category in category_array

    def desc_contains_term(self, term):
        return term in self.description

    #returns a dictionary of tags and formatted tags
    #the tag is the "normal" tag, used for display
    #the formatted tag has whitespace replaced with underscores, used in URLs
    def get_tags_to_URL_tags(self):
        return self._make_unformatted_to_formatted_dict(self.tags)

    def get_category_to_URL_category(self):
        return self._make_unformatted_to_formatted_dict(self.category)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


    #utility methods - do NOT call from outside this class!

    def _make_unformatted_to_formatted_dict(self, unformatted_string):
        unformatted_to_formatted_dict = {}
        string_param_array = self._make_string_param_array(unformatted_string)
        
        for unformatted_param in string_param_array:
            unformatted_to_formatted_dict.update(
                {unformatted_param : self._format_for_URL(unformatted_param)})
        
        return unformatted_to_formatted_dict 

 
    def _make_string_param_array(self, unformatted_string):
        return [current_param.strip() for current_param in unformatted_string.split(',')]

 
    def _format_for_URL(self, unformatted_param):
        return unformatted_param.replace(" ", "_")
        
