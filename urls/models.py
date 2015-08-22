import hashlib
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
        h = hashlib.md5()
        h.update(self.origin + self.title)
        filename = h.hexdigest() + '.png'
        self.upload(filename)
        self.save()

    def upload(self, filename):
        # instantiate PahntomJS driver
        driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
        driver.get(self.destination)
        driver.save_screenshot('/tmp/%s' % filename)
        driver.quit()
        # get and upload screenshot
        conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        key = Key(bucket)
        # generating unique hash name for the file
        h = hashlib.md5()
        h.update(self.origin + self.title)
        key.key = '/screenshots/%s' % filename
        key.set_contents_from_filename('/tmp/%s' % filename)
        bucket.set_acl('public-read', key.key)
        os.remove('/tmp/%s' % filename)
        # image URL with leading slash trimmed
        self.screenshot = 'http://cechishi-bucket.s3.amazonaws.com/' + key.key[1:]

    def __str__(self):
        return self.origin
