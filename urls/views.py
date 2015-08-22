from django.shortcuts import render, get_object_or_404, redirect
from .models import Url
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import UrlSerializer
from .forms import UrlForm
from django.contrib.auth.decorators import login_required


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
    elif request.POST.get('recapture'):
        url.upload()
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
@api_view(['GET', 'POST'])
def rest_url_list(request, format=None):
    if request.method == 'GET':
        urls = Url.objects.all()
        serializer = UrlSerializer(urls, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UrlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='/urlexpander/accounts/login/')
@api_view(['GET', 'PUT', 'DELETE'])
def rest_url_detail(request, pk, format=None):
    try:
        url = Url.objects.get(pk=pk)
    except Url.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UrlSerializer(url)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UrlSerializer(url, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required(login_url='/urlexpander/accounts/login/')
@api_view(['POST', ])
def recapture(request, pk, format=None):
    url = get_object_or_404(Url, pk=pk)
    if request.method == 'POST':
        url.upload()
