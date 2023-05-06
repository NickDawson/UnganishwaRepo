
from django.contrib import admin

from .models import Source, Headline
# Register your models here.

'''
class NewsAdmin(admin.ModelAdmin):
    list_display = ("channel_name", "title", "pub_date")
'''

admin.site.register(Source)
admin.site.register(Headline)