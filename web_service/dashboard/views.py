from django.shortcuts import render
from web_service.dashboard.eda_applications import dash_main

# Create your views here.
def home_page(request):
    return render(request, 'dashboard/welcome.html')


def personalised_page(request):
    return render(request, 'dashboard/personalised.html')