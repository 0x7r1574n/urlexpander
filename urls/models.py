from django.db import models
import requests
import bs4
from selenium import webdriver
import os


class Url(models.Model):
    origin = models.URLField()
    destination = models.URLField()
    status = models.IntegerField()
    title = models.CharField(max_length=200)
    screenshot = models.ImageField(upload_to='screenshots')

    def create(self):
        r = requests.get(self.origin)
        self.destination = r.url
        self.status = r.status_code
        self.title = bs4.BeautifulSoup(r.text).title.text
        self.screenshot = webdriver.PhantomJS(service_log_path=os.path.devnull).get(self.destination).get_screenshot_as_file('%s.png' % self.pk)
        self.save()

    def __str__(self):
        return self.origin
