from django.urls import path
from dashboard import views
from dashboard.eda_applications import dash_main

urlpatterns = [
    path('', views.home_page, name='dashboard-home'),
    path('personalised/', views.personalised_page, name='dashboard-personalised')
]