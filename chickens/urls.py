from django.urls import path
from . import views

urlpatterns = [
    path('', views.batch_list, name='batch_list'),
    path('add/', views.add_batch, name='add_batch'),
    path('edit/<int:batch_id>/', views.edit_batch, name='edit_batch'),
    path('delete/<int:batch_id>/', views.delete_batch, name='delete_batch'),
]