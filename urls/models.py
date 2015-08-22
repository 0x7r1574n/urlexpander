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
        title_tag = bs4.BeautifulSoup(r.text).title
        if title_tag:
            self.title = title_tag.text
        else:
            self.title = 'None'
        driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
        driver.get(self.destination)
        self.screenshot = driver.save_screenshot('%s.png' % self.pk)
        driver.quit()
        self.save()

    def __str__(self):
        return self.origin
