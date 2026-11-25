from orders.views import available_egg_count
from orders.models import EggOrder
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.db.models import Sum

from chickens.models import ChickenBatch
from production.models import EggProduction
from feed.models import FeedStock

from .forms import RegisterForm, ProfileUpdateForm


# Admin Dashboard
@login_required
def dashboard(request):

    # Redirect customers to Customer Dashboard
    if not request.user.is_staff:
        return redirect('customer_dashboard')

    total_batches = ChickenBatch.objects.count()

    total_production_records = EggProduction.objects.count()

    total_feed_stock = FeedStock.objects.aggregate(
        total=Sum('quantity_kg')
    )['total'] or 0

    context = {
        'total_batches': total_batches,
        'total_production_records': total_production_records,
        'feed_stock': total_feed_stock,
    }

    return render(request, 'dashboard.html', context)


@login_required
def customer_dashboard(request):

    if request.user.is_staff:
        return redirect('dashboard')

    available = available_egg_count()

    latest_order = EggOrder.objects.filter(
        customer=request.user
    ).order_by('-order_date').first()

    return render(
        request,
        'customer_dashboard.html',
        {
            'available_eggs': available,
            'latest_order': latest_order
        }
    )



    # Calculate good eggs
    totals = EggProduction.objects.aggregate(
        total_collected=Sum('eggs_collected'),
        total_damaged=Sum('damaged_eggs')
    )

    total_collected = totals['total_collected'] or 0
    total_damaged = totals['total_damaged'] or 0

    total_good_eggs = max(
        total_collected - total_damaged,
        0
    )

    context = {
        'available_eggs': total_good_eggs,
    }

    return render(
        request,
        'customer_dashboard.html',
        context
    )


# Register Customer
def register(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            user.is_staff = False
            user.is_superuser = False
            user.save(update_fields=['is_staff', 'is_superuser'])

            login(request, user)

            return redirect('dashboard')

    else:
        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


# User Profile
@login_required
def profile(request):
    return render(request, 'profile.html')


# Edit Profile
@login_required
def edit_profile(request):

    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Profile updated successfully!"
            )

            return redirect('profile')

    else:
        form = ProfileUpdateForm(
            instance=request.user
        )

    return render(
        request,
        'edit_profile.html',
        {'form': form}
    )


# Change Password
@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Password changed successfully!"
            )

            return redirect('profile')

    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        'change_password.html',
        {'form': form}
    )
