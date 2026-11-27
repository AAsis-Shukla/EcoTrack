from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),

    path(
        'management/',
        views.management_dashboard,
        name='management_dashboard'
    ),

    path(
        'donor/',
        views.donor_dashboard,
        name='donor_dashboard'
    ),
]