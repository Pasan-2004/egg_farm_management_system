
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.db.models.deletion import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404

from .models import ChickenBatch
from .forms import ChickenBatchForm


# Admin permission decorator
def admin_required(view_func):

    @user_passes_test(lambda user: user.is_authenticated)
    def protected_view(request, *args, **kwargs):

        if not request.user.is_staff:
            raise PermissionDenied(
                "Only farm administrators can access this page."
            )

        return view_func(request, *args, **kwargs)

    return protected_view


# 1. Display all chicken batches
@admin_required
def batch_list(request):

    batches = ChickenBatch.objects.all()

    return render(
        request,
        'chickens/batch_list.html',
        {'batches': batches}
    )


# 2. Add new chicken batch
@admin_required
def add_batch(request):

    if request.method == 'POST':
        form = ChickenBatchForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Chicken batch added successfully!"
            )

            return redirect('batch_list')

    else:
        form = ChickenBatchForm()

    return render(
        request,
        'chickens/add_batch.html',
        {'form': form}
    )


# 3. Edit existing chicken batch
@admin_required
def edit_batch(request, batch_id):

    batch = get_object_or_404(
        ChickenBatch,
        id=batch_id
    )

    if request.method == 'POST':
        form = ChickenBatchForm(
            request.POST,
            instance=batch
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Chicken batch updated successfully!"
            )

            return redirect('batch_list')

    else:
        form = ChickenBatchForm(
            instance=batch
        )

    return render(
        request,
        'chickens/add_batch.html',
        {'form': form}
    )


# 4. Delete chicken batch
@admin_required
def delete_batch(request, batch_id):

    batch = get_object_or_404(
        ChickenBatch,
        id=batch_id
    )

    if request.method == 'POST':

        try:
            batch.delete()

            messages.success(
                request,
                "Chicken batch deleted successfully!"
            )

        except ProtectedError:

            messages.error(
                request,
                "Cannot delete this batch because "
                "it is used in other farm records."
            )

        return redirect('batch_list')

    return render(
        request,
        'chickens/delete_batch.html',
        {'batch': batch}
    )
