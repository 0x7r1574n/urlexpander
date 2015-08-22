from django.shortcuts import render, get_object_or_404, redirect
from .models import Url
from .serializers import UrlSerializer
from .forms import UrlForm
from django.contrib.auth.decorators import login_required
from rest_framework import generics


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
            url.create()
            return redirect('urls.views.url_detail', pk=url.pk)
    else:
        form = UrlForm()
    return render(request, 'urls/url_add.html', {'form': form})


@login_required(login_url='/urlexpander/accounts/login/')
class UrlList(generics.ListCreateAPIView):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer


@login_required(login_url='/urlexpander/accounts/login/')
class UrlDetail(generics.RetrieveDestroyAPIView):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer


@login_required(login_url='/urlexpander/accounts/login/')
def recapture(request, pk):
    url = get_object_or_404(Url, pk=pk)
    if request.method == 'POST':
        url.upload()
