from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return HttpResponse('<h1>Hello World Django!</h1>')


def about_page(request):
    return HttpResponse('<h1>Project Introduction</h1>')