
from django.shortcuts import render, redirect, get_object_or_404
from .models import ChickenBatch
from .forms import ChickenBatchForm


# 1. Display all chicken batches
def batch_list(request):
    batches = ChickenBatch.objects.all()

    return render(request, 'chickens/batch_list.html', {
        'batches': batches
    })


# 2. Add new chicken batch
def add_batch(request):
    if request.method == 'POST':
        form = ChickenBatchForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('batch_list')
    else:
        form = ChickenBatchForm()

    return render(request, 'chickens/add_batch.html', {
        'form': form
    })


# 3. Edit existing chicken batch
def edit_batch(request, batch_id):
    batch = get_object_or_404(ChickenBatch, id=batch_id)

    if request.method == 'POST':
        form = ChickenBatchForm(request.POST, instance=batch)

        if form.is_valid():
            form.save()
            return redirect('batch_list')
    else:
        form = ChickenBatchForm(instance=batch)

    return render(request, 'chickens/add_batch.html', {
        'form': form
    })


# 4. Delete chicken batch
def delete_batch(request, batch_id):
    batch = get_object_or_404(ChickenBatch, id=batch_id)

    if request.method == 'POST':
        batch.delete()
        return redirect('batch_list')

    return render(request, 'chickens/delete_batch.html', {
        'batch': batch
    })


