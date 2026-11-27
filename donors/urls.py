
from django.urls import path
from . import views

app_name = 'donors'

urlpatterns = [
    path('', views.donor_list, name='donor_list'),
    path('<int:pk>/', views.donor_detail, name='donor_detail'),
    path('<int:pk>/approve/', views.donor_approve, name='donor_approve'),
    path('<int:pk>/reject/', views.donor_reject, name='donor_reject'),
    path(
        '<int:pk>/toggle-status/',
        views.donor_toggle_status,
        name='donor_toggle_status'
    ),
]
