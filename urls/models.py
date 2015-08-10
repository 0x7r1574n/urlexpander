from django.db import models
import requests
import bs4


class Url(models.Model):
    origin = models.URLField()
    destination = models.URLField()
    status = models.IntegerField()
    title = models.CharField(max_length=200)

    def create(self):
        r = requests.get(self.origin)
        self.destination = r.url
        self.status = r.status_code
        self.title = bs4.BeautifulSoup(r.text).title.text
        self.save()

    def __str__(self):
        return self.origin
