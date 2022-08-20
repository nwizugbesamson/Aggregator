from django.shortcuts import render


# Create your views here.
def home_page(request):
    return render(request, 'dashboard/welcome.html')


def about_page(request):
    return render(request, 'dashboard/welcome.html')