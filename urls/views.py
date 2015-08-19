from django.shortcuts import render, get_object_or_404, redirect
from .models import Url
from .serializers import UrlSerializer
from .forms import UrlForm
from django.contrib.auth.decorators import login_required
from rest_framework import generics
import requests
import bs4
from selenium import webdriver


@login_required(login_url='/urlexpander/accounts/login/')
def url_list(request):
    urls = Url.objects.all()
    return render(request, 'urls/url_list.html', {'urls': urls})


@login_required(login_url='/urlexpander/accounts/login/')
def url_detail(request, pk):
    url = get_object_or_404(Url, pk=pk)
    if request.POST.get('delete'):
        url.delete()
        return redirect('urls.views.url_list')
    return render(request, 'urls/url_detail.html', {'url': url})


@login_required(login_url='/urlexpander/accounts/login/')
def url_add(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            r = requests.get(url.origin)
            url.destination = r.url
            url.status = r.status_code
            title_tag = bs4.BeautifulSoup(r.text).title
            url.screenshot = webdriver.PhantomJS().get(url.destination).get_screenshot_as_file('%s.png' % url.pk)
            if title_tag:
                url.title = title_tag.text
            else:
                url.title = 'None'
            url.save()
            return redirect('urls.views.url_detail', pk=url.pk)
    else:
        form = UrlForm()
    return render(request, 'urls/url_add.html', {'form': form})


class UrlList(generics.ListCreateAPIView):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer


class UrlDetail(generics.RetrieveDestroyAPIView):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer


def recapture(request, pk):
    url = get_object_or_404(Url, pk=pk)
    if request.method == 'POST':
        url.screenshot = webdriver.PhantomJS().get(url.destination).get_screenshot_as_file('%s.png' % pk)
