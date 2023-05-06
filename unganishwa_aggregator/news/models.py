from django.db import models
from django.utils import timezone
# Create your models here.
'''
class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    channel_name = models.CharField(max_length=100)
    guid = models.CharField(max_length=50)

    #def __str__(self) -> str:
    #   return f"{self.channel_name}: {self.title}"

    def __str__(self) -> str:
        return self.title
'''

'''
class News(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null=True, blank=True)
    url = models.TextField()

    def __str__(self):
        return self.title
'''

class Source(models.Model):
    source_name = models.CharField(max_length=100)
    source_link = models.TextField()
    source_category = models.CharField(max_length=100)
    updated_datetime = models.DateTimeField(default=timezone.now)


class Headline(models.Model):
    source = models.ForeignKey('news.Source', related_name='news', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    link = models.TextField()


    def __str__(self) -> str:
        return self.title

