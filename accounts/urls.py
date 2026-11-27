from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),

    path(
        'register/management/',
        views.management_register,
        name='management_register'
    ),

    path(
        'register/donor/',
        views.donor_register,
        name='donor_register'
    ),

    path(
        'login/',
        views.EcoTrackLoginView.as_view(),
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),
]