
from django.urls import path
from . import views

urlpatterns = [
    path('', views.production_list, name='production_list'),
    path('add/', views.add_production, name='add_production'),
    path('edit/<int:pk>/', views.edit_production, name='edit_production'),
    path('delete/<int:pk>/', views.delete_production, name='delete_production'),
]
