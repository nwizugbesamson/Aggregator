from django.urls import path
from web_service.dashboard import views

urlpatterns = [
    path('', views.home_page, name='dashboard-home')
]