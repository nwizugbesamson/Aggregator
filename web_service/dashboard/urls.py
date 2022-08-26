from django.urls import path
from web_service.dashboard import views
from web_service.dashboard.eda_applications import dash_main
from web_service.dashboard.eda_applications.dash_main import personalised_app

urlpatterns = [
    path('', views.home_page, name='dashboard-home'),
    path('personalised/', views.personalised_page, name='dashboard-personalised')
]