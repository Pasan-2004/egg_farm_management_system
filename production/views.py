from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import EggProduction
from .forms import EggProductionForm


# Display all egg production records
@login_required

def production_list(request):
    productions = EggProduction.objects.all().order_by('-date', '-id')

    return render(
        request,
        'production/production_list.html',
        {'productions': productions}
    )


# Add new egg production
@login_required
def add_production(request):
    if request.method == 'POST':
        form = EggProductionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('production_list')
    else:
        form = EggProductionForm()

    return render(
        request,
        'production/production_form.html',
        {
            'form': form,
            'title': 'Add Egg Production'
        }
    )


# Edit existing egg production
@login_required
def edit_production(request, pk):
    production = get_object_or_404(EggProduction, pk=pk)

    if request.method == 'POST':
        form = EggProductionForm(request.POST, instance=production)

        if form.is_valid():
            form.save()
            return redirect('production_list')
    else:
        form = EggProductionForm(instance=production)

    return render(
        request,
        'production/production_form.html',
        {
            'form': form,
            'title': 'Edit Egg Production'
        }
    )


# Delete egg production
@login_required
def delete_production(request, pk):
    production = get_object_or_404(EggProduction, pk=pk)

    if request.method == 'POST':
        production.delete()
        return redirect('production_list')

    return render(
        request,
        'production/delete_production.html',
        {'production': production}
    )
