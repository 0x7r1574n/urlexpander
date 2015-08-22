from tempfile import TemporaryFile
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
        self.upload()
        self.save()

    def upload(self):
        # instantiate PahntomJS driver
        driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
        driver.get(self.destination)
        temp_file = TemporaryFile()
        temp_file.write(driver.get_screenshot_as_png())
        driver.quit()
        # get and upload screenshot
        conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        key = Key(bucket)
        # generating unique hash name for the file
        h = hashlib.md5()
        h.update(self.origin + self.title)
        key.key = '/screenshots/%s.png' % h.hexdigest()
        key.set_contents_from_file(temp_file)
        bucket.set_acl('public-read', key.key)
        temp_file.close()
        # image URL with leading slash trimmed
        self.screenshot = settings.STATIC_URL + key.key[1:]

    def __str__(self):
        return self.origin
