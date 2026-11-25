
from django.urls import path
from . import views


urlpatterns = [
    path('', views.health_list, name='health_list'),

    path('add/', views.add_health, name='add_health'),

    path(
        'edit/<int:pk>/',
        views.edit_health,
        name='edit_health'
    ),

    path(
        'delete/<int:pk>/',
        views.delete_health,
        name='delete_health'
    ),
]
