from django.urls import path
from web_service.dashboard import views

urlpatterns = [
    path('', views.home_page, name='dashboard-home'),
    path('about/', views.about_page, name='dashboard-author')
]