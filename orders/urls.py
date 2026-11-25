
from django.urls import path
from . import views

urlpatterns = [
    path(
        'place/',
        views.place_order,
        name='place_order'
    ),

    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),

    path(
        'admin-orders/',
        views.admin_orders,
        name='admin_orders'
    ),
    path(
    'notifications/',
    views.notifications_list,
    name='notifications_list'
),

path(
    'notifications/<int:notification_id>/read/',
    views.mark_notification_read,
    name='mark_notification_read'
),
    path(
        'update/<int:order_id>/',
        views.update_order_status,
        name='update_order_status'
    ),
]
