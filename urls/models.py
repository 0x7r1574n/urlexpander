from django.db import models
import requests
import bs4
from selenium import webdriver
import os
from urlexpander import settings
import boto
from boto.s3.key import Key


class Url(models.Model):
    origin = models.URLField()
    destination = models.URLField()
    status = models.IntegerField()
    title = models.CharField(max_length=200)
    screenshot = models.URLField()

    def create(self):
        r = requests.get(self.origin)
        self.destination = r.url
        self.status = r.status_code
        title_tag = bs4.BeautifulSoup(r.text).title
        if title_tag:
            self.title = title_tag.text
        else:
            self.title = 'None'
        self.upload()
        self.save()

    def upload(self):
        # instantiate PahntomJS driver
        driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
        driver.get(self.destination)
        # get and upload screenshot
        conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        key = Key(bucket)
        key.key = '/screenshots/%s.png' % self.pk
        key.set_contents_from_stream(driver.get_screenshot_as_base64())
        # close PhantomJS driver
        driver.quit()
        bucket.set_acl('public-read', key.key)
        # image URL with leading slash trimmed
        self.screenshot = settings.STATIC_URL + key.key[1:]

    def __str__(self):
        return self.origin
