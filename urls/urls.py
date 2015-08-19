from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.url_list, name='url_list'),
    url(r'^url/(?P<pk>[0-9]+)/$', views.url_detail, name='url_detail'),
    url(r'^url/new/$', views.url_add, name='url_add'),
    url(r'^api/$', views.UrlList.as_view(), name='url-list'),
    url(r'^api/(?P<pk>[0-9]+)/$', views.UrlDetail.as_view(), name='url-detail'),
    url(r'^recapture/(?P<pk>[0-9]+)$', views.recapture, name='screenshot_recapture')
]
