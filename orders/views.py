
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from production.models import EggProduction

from .models import EggOrder, Notification, EggPrice
from .forms import EggOrderForm


# =====================================
# AVAILABLE EGG COUNT
# =====================================

def available_egg_count():

    production = EggProduction.objects.aggregate(
        collected=Sum('eggs_collected'),
        damaged=Sum('damaged_eggs')
    )

    collected = production['collected'] or 0
    damaged = production['damaged'] or 0

    confirmed = EggOrder.objects.filter(
        status='Confirmed'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    available = collected - damaged - confirmed

    return max(available, 0)


# =====================================
# ADMIN NOTIFICATION
# =====================================

def notify_admins(order):

    User = get_user_model()

    admins = User.objects.filter(
        is_staff=True,
        is_active=True
    )

    for admin in admins:

        Notification.objects.create(
            recipient=admin,
            order=order,
            message=(
                f"New Egg Order #{order.id}: "
                f"{order.quantity} eggs ordered by "
                f"{order.customer.username}."
            )
        )


# =====================================
# CUSTOMER NOTIFICATION
# =====================================

def notify_customer(order):

    if order.status == 'Confirmed':

        message = (
            f"Your Egg Order #{order.id} "
            f"has been confirmed successfully!"
        )

    elif order.status == 'Rejected':

        message = (
            f"Your Egg Order #{order.id} "
            f"has been rejected."
        )

    else:
        return

    Notification.objects.create(
        recipient=order.customer,
        order=order,
        message=message
    )


# =====================================
# CUSTOMER - PLACE ORDER
# =====================================

@login_required
def place_order(request):

    if request.user.is_staff:
        raise PermissionDenied

    available = available_egg_count()

    egg_price = EggPrice.objects.order_by(
        '-updated_at', '-pk'
    ).first()

    unit_price = (
        egg_price.price_per_egg
        if egg_price
        else None
    )

    if request.method == 'POST':

        form = EggOrderForm(request.POST)

        if form.is_valid():

            quantity = form.cleaned_data['quantity']

            if unit_price is None:
                messages.error(
                    request,
                    "Egg price has not been set yet."
                )

            elif unit_price <= 0:
                messages.error(
                    request,
                    "Egg price is not valid."
                )

            elif quantity > available:

                form.add_error(
                    'quantity',
                    'Requested quantity exceeds available eggs.'
                )

            else:

                with transaction.atomic():

                    order = form.save(commit=False)

                    order.customer = request.user
                    order.status = 'Pending'

                    order.save()

                    notify_admins(order)

                messages.success(
                    request,
                    "Your egg order has been placed successfully!"
                )

                return redirect('my_orders')

    else:
        form = EggOrderForm()

    return render(
        request,
        'orders/place_order.html',
        {
            'form': form,
            'available_eggs': available,
            'egg_price': unit_price if unit_price is not None else 0,
            'price_is_set': (
                unit_price is not None and unit_price > 0
            ),
        }
    )


# =====================================
# CUSTOMER - MY ORDERS
# =====================================

@login_required
def my_orders(request):

    if request.user.is_staff:
        raise PermissionDenied

    orders = EggOrder.objects.filter(
        customer=request.user
    ).order_by('-order_date')

    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders
        }
    )


# =====================================
# ADMIN - ALL CUSTOMER ORDERS
# =====================================

@login_required
def admin_orders(request):

    if not request.user.is_staff:
        raise PermissionDenied

    orders = EggOrder.objects.select_related(
        'customer'
    ).order_by('-order_date')

    return render(
        request,
        'orders/admin_orders.html',
        {
            'orders': orders,
            'available_eggs': available_egg_count()
        }
    )


# =====================================
# ADMIN - CONFIRM / REJECT ORDER
# =====================================

@login_required
def update_order_status(request, order_id):

    if not request.user.is_staff:
        raise PermissionDenied

    if request.method != 'POST':
        return redirect('admin_orders')

    action = request.POST.get('action')

    if action not in ['Confirmed', 'Rejected']:

        messages.error(
            request,
            "Invalid order action."
        )

        return redirect('admin_orders')

    with transaction.atomic():

        order = get_object_or_404(
            EggOrder.objects.select_for_update(),
            id=order_id
        )

        if order.status != 'Pending':

            messages.warning(
                request,
                "This order has already been processed."
            )

        elif action == 'Confirmed':

            available = available_egg_count()

            if order.quantity > available:

                messages.error(
                    request,
                    "Not enough eggs available to confirm this order."
                )

            else:

                order.status = 'Confirmed'
                order.save(update_fields=['status'])

                notify_customer(order)

                messages.success(
                    request,
                    "Order confirmed successfully!"
                )

        elif action == 'Rejected':

            order.status = 'Rejected'
            order.save(update_fields=['status'])

            notify_customer(order)

            messages.success(
                request,
                "Order rejected successfully."
            )

    return redirect('admin_orders')


# =====================================
# NOTIFICATIONS PAGE
# =====================================

@login_required
def notifications_list(request):

    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')

    unread_count = notifications.filter(
        is_read=False
    ).count()

    return render(
        request,
        'orders/notifications.html',
        {
            'notifications': notifications,
            'unread_count': unread_count
        }
    )


# =====================================
# MARK NOTIFICATION AS READ
# =====================================

@login_required
def mark_notification_read(request, notification_id):

    if request.method != 'POST':
        return redirect('notifications_list')

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )

    notification.is_read = True
    notification.save(update_fields=['is_read'])

    return redirect('notifications_list')
