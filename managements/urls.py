
from django.urls import path
from . import views

app_name = 'managements'

urlpatterns = [
    path('zones/', views.zone_list, name='zone_list'),
    path('zones/add/', views.zone_create, name='zone_create'),
    path('zones/<int:pk>/edit/', views.zone_update, name='zone_update'),
    path(
        'zones/<int:pk>/toggle-status/',
        views.zone_toggle_status,
        name='zone_toggle_status'
    ),
    path('zones/<int:pk>/delete/', views.zone_delete, name='zone_delete'),
]
