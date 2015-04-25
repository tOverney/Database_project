from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. This is live from a python" +
        " script through django, throught uwsgi")
