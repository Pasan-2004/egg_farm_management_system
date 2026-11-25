
from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_list, name='feed_list'),
    path('add/', views.add_feed, name='add_feed'),
    path(
        'consumption/add/',
        views.add_consumption,
        name='add_consumption'
    ),
]
