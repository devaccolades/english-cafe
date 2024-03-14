from django.contrib import admin
from general.models import *

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name','web_code','flag','phone_code','phone_number_length')
    search_fields = ('name', 'web_code')

admin.site.register(Country,CountryAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('auto_id', 'id', 'created_at', 'title', 'description', 'thumbnail', 'image', 'date_added', 'author', 'meta_title', 'meta_description', 'slug')
    ordering = ('auto_id',)
    search_fields = ('tags', 'title')

admin.site.register(Blog, BlogAdmin)


class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Tags,TagsAdmin)