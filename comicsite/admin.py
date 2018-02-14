from django.contrib import admin

from .models import Blogpost

class BlogpostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Blogpost, BlogpostAdmin)

# Register your models here.
